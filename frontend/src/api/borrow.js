import request from '../utils/request'

export const getBorrowRecordsApi = params => request.get('/borrow-records', { params })
export const getMyBorrowRecordsApi = params => request.get('/borrow-records/my', { params })
export const borrowBookApi = data => request.post('/borrow-records/borrow', data)
export const returnBookApi = id => request.post(`/borrow-records/return/${id}`)

