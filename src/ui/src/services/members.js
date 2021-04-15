export const baseURL = process.env.VUE_APP_ROOT_API_URL || '/'
export const apiUrl = '/v1/employee'

const config = {
  FETCH_MEMBER_LIST: '/fetch/',
  ADD_MEMBER: '/create/',
  DELETE_MEMBER: '/delete/',
}

export const getList = async () => {
  const response = await fetch(`${baseURL}${apiUrl}${config.FETCH_MEMBER_LIST}`)
  return await response.json()
}

export const addUser = async user => {
  const response = await fetch(`${baseURL}${apiUrl}${config.ADD_MEMBER}`, {
    method: 'POST',
    body: JSON.stringify(user)
  })

  if(response.status !== 200) throw new Error(response)

  return await response.json()
}

export const deleteUser = async id => {
  /* eslint-disable no-debugger */
  const response = await fetch(`${baseURL}${apiUrl}/${id}${config.DELETE_MEMBER}`, {
    method: 'DELETE',
    body: id
  })

  return await response.json()
}
