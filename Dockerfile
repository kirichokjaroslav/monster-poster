FROM node:lts-alpine AS build

WORKDIR /src

COPY src/ui/ /src

RUN npm install
RUN npm run build

# -----------------------------------
FROM nginx:latest

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/dist /app/
