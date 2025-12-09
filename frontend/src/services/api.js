// Simple Axios client that always talks to the real Flask backend

import axios from 'axios'

// IMPORTANT: backend must be running at http://127.0.0.1:5000
const api = axios.create({
  baseURL: import.meta.env.DEV 
    ? 'http://127.0.0.1:5000/api' 
    : 'https://recipe-repository-1.onrender.com/api',  // ← YOUR LIVE BACKEND
  timeout: 10000,
  withCredentials: true,
})

export default api
