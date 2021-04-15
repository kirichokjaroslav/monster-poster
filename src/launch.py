from __future__ import with_statement

import os
import random
import sys
from multiprocessing import active_children
from os import path
from typing import Any, Callable, Dict, cast
from uuid import uuid4

import dateparser as dp
import pendulum as pm
import slack
from apscheduler import events
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, Response, request
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont
from returns.result import safe

import helpers
import settings as se
from api.models import DatabaseConnector, EmployeeModel
from api.views import employee_blueprint


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


def add_cors_headers(response: Response) -> Response:
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


def create_greeting_poster(
    poster: Dict[str, Any], photography: str, name: str, years: int
) -> str:
    """The function creates a greeting poster based on the selected poster
    and employee data.

    Args:
        poster: Random selected poster
        photography: Path to photography employee
        name: Name employee
        years: Years count employee in the company

    Returns:
        If the poster was successfully created and saved, return the path
        to the poster.
    """
    def draw_text(free_text: str = '', *, item: Dict[str, Any]) -> None:
        font = ImageFont.truetype(path.join(se.shared.FONTS_DIR, f'''{item.get('font-family')}.ttf'''),
                                  item.get('font-size'),
                                  encoding='utf-8')
        # If the free text is not specified, try to take the text from the template
        width_font, _ = font.getsize(free_text or item.get('text'))
        _, height_font = font.getoffset(free_text or item.get('text'))
        # ... and draw text
        draw.text(((poster_im_width - width_font) // 2, item.get('y') - height_font),
                  free_text or item.get('text'),
                  ImageColor.getrgb(item.get('color')),
                  font=font)

    # Safety open a poster image
    with Image.open(path.join(se.shared.POSTERS_DIR, poster.get('image'))) as poster_im:
        # Get width and height poster image
        poster_im_width, _ = poster_im.size
        try:
            with Image.open(photography) as photography_im:
                # Get size image for define offset
                photography_im_width, _ = photography_im.size
                offset = ((poster_im_width - photography_im_width) // 2,
                          poster.get('items', {}).get('photography', {}).get('y'))
                # Convert image to grayscale
                photography_im_gray = photography_im.convert('LA')
                poster_im.paste(photography_im_gray, offset, photography_im)
        except BaseException:
            se.logger.error(
                'An error occurred, while opening the photography; Continue without photography')
        # ... and let's go drawing text
        draw = ImageDraw.Draw(poster_im)
        draw_text(free_text=name,
                  item=poster.get('items', {}).get('name', {}))
        draw_text(item=poster.get('items', {}).get('congratulations', {}))
        draw_text(item=poster.get('items', {}).get('summary', {}))
        draw_text(free_text=str(years),
                  item=poster.get('items', {}).get('years', {}).get('count', {}))
        draw_text(free_text=helpers.time_interpreter(years),
                  item=poster.get('items', {}).get('years', {}).get('below', {}))
        # Formed file name
        path_to_poster = path.join(se.shared.BUILT_POSTERS_DIR, f'{uuid4().hex}.jpg')
        # ... and save image
        poster_im.save(path_to_poster)

    return path_to_poster or ''


def scheduler_job_greeting_persistent() -> None:
    """The general function of checking, creating and sending a greeting
    poster in Slack.
    """
    with DatabaseConnector(se.DatabaseEngines.SQLITE) as dbs:
        if dbs.enter_to_context:
            # Create model and traverse on all empoloyees
            employee_model = EmployeeModel(dbs.session)
            employees = employee_model.get_employees()
            for employee in employees:
                # Get in_company_from date field and check it with now date
                compare_dt = dp.parse(employee.in_company_from)
                if all([compare_dt.date().day   == pm.now().date().day,
                        compare_dt.date().month == pm.now().date().month]):
                    # First, get random poster
                    posters = se.shared.file_vars.pluck('posters')
                    single_poster_key = random.choice(list(posters.keys()))
                    # Then we transfer this poster and some employee data to the function
                    # of creating a poster
                    single_poster_obj: \
                        Dict[str, Any] = posters.get(single_poster_key)
                    # Some employee personal data
                    photography = f'{se.shared.BASE_DIR}{employee.photography}'
                    name = f'{employee.first_name}\u0020{employee.last_name}'
                    years = pm.now().date().diff(compare_dt.date()).years
                    # ... and try create greeting poster
                    path_to_poster = \
                        create_greeting_poster(single_poster_obj, photography, name, years)
                    # If the poster is created, - send it to Slack
                    is_sended: bool = False
                    if path_to_poster:
                        # Get target channel
                        channel = \
                            se.shared.file_vars.pluck('messenger').get('channel')
                        # Trying send greeting poster
                        is_sended = send_a_greeting_poster(f'#{channel}', path_to_poster)
                    # ... and clean up the files
                    if is_sended:
                        helpers.remove_file(path_to_poster)
        else:
            se.logger.error('Oops! Something went wrong with the database.')


def scheduler_job_run_monitoring(event: events.JobEvent) -> None:
    """Listener-function that tracks events occurring in the scheduler.

    Args:
        event: Event that occurred in the scheduler

    Returns:
        Returns response status like True or False
    """
    if 'grabbing.persistent' in event.job_id:
        suitable_event_job: Callable[..., bool] = {
            events.EVENT_JOB_EXECUTED:  lambda: scheduler.is_busy or False,
            events.EVENT_JOB_SUBMITTED: lambda: scheduler.is_busy or True
        }.get(event.code, lambda: False)
        # ... and call scheduler jobs state function
        suitable_event_job()


def send_a_greeting_poster(channel: str, path_to_poster: str) -> bool:
    """Function of sending greeting poster to the channel Slack.

    Args:
        channel: Specify Slack channel
        path_to_poster: Employee generated greeting poster

    Returns:
        Returns response status like True or False
    """
    response = \
        slack_client.files_upload(channels=channel, file=path_to_poster)
    return cast(bool, response.get('ok', False))


def send_a_text(channel: str, text: str) -> bool:
    """Function of sending messages to the channel Slack.

    Args:
        channel: Specify Slack channel
        text: Message text to send
    """
    response = \
        slack_client.chat_postMessage(channel=channel, text=text)
    return cast(bool, response.get('ok', False))


server = Flask(__name__, static_url_path='/static')
server.after_request(add_cors_headers)
server.register_blueprint(employee_blueprint)

# Create scheduler
scheduler = BackgroundScheduler({'apscheduler.executors.default': {
                                    'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                                    'max_workers': se.shared.MAX_SCHEDULER_WORKERS},
                                 'apscheduler.timezone': pm.now().timezone_name})
# This variable is needed to indicate whether there was a rescheduling of
# the persistent job in the scheduler
setattr(scheduler, 'emergency_mode', False)
setattr(scheduler, 'is_busy', False)

# Get Slack ``xoxb-*`` OAuth Access Token
slack_xoxb_access = se.shared.file_vars.pluck('messenger').get('xoxb')
# Create Slack client
slack_client = slack.WebClient(token=slack_xoxb_access)


if __name__ == '__main__':
    try:
        # Read the settings for the crown from the global settings ``keeper``
        # and create a job in the scheduler with these settings
        run_every = \
            se.shared.file_vars.pluck('properties').get('run_every')
        scheduler.start()
        scheduler.add_job(scheduler_job_greeting_persistent,
                          trigger=CronTrigger.from_crontab(run_every),
                          id='greeting.persistent',
                          coalesce=True)
        scheduler.add_listener(
            scheduler_job_run_monitoring, events.EVENT_JOB_EXECUTED |
                                          events.EVENT_JOB_SUBMITTED)
        # ... and serve Bottle
        se.logger.info(':: Start TCP server ::')
        server.run(host=se.shared.HOST,
                   port=se.shared.PORT,
                   debug=se.shared.DEBUG,
                   load_dotenv=False,
                   use_reloader=se.shared.DEBUG,
                   use_debugger=se.shared.DEBUG)
    except KeyboardInterrupt:
        se.logger.error('KeyboardInterrupt has been caught; wait, cleaning up...')
        sys.exit(os.EX_SOFTWARE)
    finally:
        # Breaking scheduler all jobs
        scheduler.remove_all_jobs()
        scheduler.shutdown() if scheduler.running else (lambda: None)()
        # Breaking all sub processes
        se.logger.info(':: Clean everything sub processes ::')
        for child in active_children():
            child.terminate()
