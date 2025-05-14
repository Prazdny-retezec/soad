// src/services/api.js
import axios from 'axios'

const { VITE_API_URL, VITE_ADMIN_USERNAME, VITE_ADMIN_PASSWORD } = import.meta.env

axios.defaults.baseURL = VITE_API_URL

axios.interceptors.request.use(req => {
  const token = btoa(`${VITE_ADMIN_USERNAME}:${VITE_ADMIN_PASSWORD}`)
  req.headers.Authorization = `Basic ${token}`
  return req
})

export default axios
