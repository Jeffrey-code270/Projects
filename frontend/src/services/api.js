import axios from 'axios';

const API_URL = '/api';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (credentials) => api.post('/auth/register', credentials),
};

export const notes = {
  getAll: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return api.get(`/notes${query ? `?${query}` : ''}`);
  },
  create: (note) => api.post('/notes', note),
  update: (id, note) => api.put(`/notes/${id}`, note),
  delete: (id) => api.delete(`/notes/${id}`),
  pin: (id, isPinned) => api.put(`/notes/${id}/pin`, { isPinned }),
  favorite: (id, isFavorite) => api.put(`/notes/${id}/favorite`, { isFavorite }),
  share: (id, isPublic) => api.put(`/notes/${id}/share`, { isPublic }),
  getShared: (shareId) => api.get(`/notes/shared/${shareId}`),
  getStats: () => api.get('/notes/stats'),
  getAnalytics: () => api.get('/notes/analytics'),
};

export const user = {
  updateUsername: (username) => api.put('/user/update-username', { username }),
};

export default api;