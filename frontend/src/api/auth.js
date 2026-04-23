import request from '../utils/request'

export const loginApi = data => request.post('/auth/login', data)
export const meApi = () => request.get('/auth/me')
export const updateProfileApi = data => request.put('/auth/profile', data)
export const changePasswordApi = data => request.put('/auth/change-password', data)

