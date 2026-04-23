import request from '../utils/request'

export const getBooksApi = params => request.get('/books', { params })
export const getBookApi = id => request.get(`/books/${id}`)
export const createBookApi = data => request.post('/books', data)
export const updateBookApi = (id, data) => request.put(`/books/${id}`, data)
export const deleteBookApi = id => request.delete(`/books/${id}`)
export const uploadCoverApi = file => {
  const form = new FormData()
  form.append('file', file)
  return request.post('/upload/cover', form, { headers: { 'Content-Type': 'multipart/form-data' } })
}

