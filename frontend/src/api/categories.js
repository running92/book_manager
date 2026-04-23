import request from '../utils/request'

export const getCategoriesApi = () => request.get('/categories')
export const createCategoryApi = data => request.post('/categories', data)
export const updateCategoryApi = (id, data) => request.put(`/categories/${id}`, data)
export const deleteCategoryApi = id => request.delete(`/categories/${id}`)

