import axios from 'axios';

// In dev: '/api' (uses Vite proxy)
// In production: set VITE_API_URL to your Render backend URL
const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({ baseURL: API_BASE });

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auth
export const registerUser = (data) => api.post('/auth/register', data);
export const loginUser = (data) => api.post('/auth/login', data);

// Resume
export const uploadResume = (file) => {
  const fd = new FormData();
  fd.append('file', file);
  return api.post('/resume/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
};
export const getResume = (id) => api.get(`/resume/${id}`);
export const listResumes = () => api.get('/resume/');

// ATS
export const scoreResume = (resume_id) => api.post('/ats/score', { resume_id });
export const getScoreHistory = (resume_id) => api.get(`/ats/history/${resume_id}`);

// Domain
export const getDomains = () => api.get('/domains');
export const selectDomain = (resume_id, domain) => api.post('/domain/select', { resume_id, domain });

// Skills
export const getExtractedSkills = (resume_id) => api.get(`/skills/extracted?resume_id=${resume_id}`);
export const getSkillGap = (resume_id) => api.get(`/skills/gap?resume_id=${resume_id}`);

// Roadmap
export const generateRoadmap = (resume_id) => api.get(`/roadmap/generate?resume_id=${resume_id}`);
export const getRoadmap = (user_id) => api.get(`/roadmap/${user_id}`);
export const completeWeek = (roadmap_id, is_completed) => api.patch('/roadmap/week/complete', { roadmap_id, is_completed });

// Dashboard
export const getDashboard = (user_id) => api.get(`/dashboard/${user_id}`);

// Admin
export const getAdminStats = () => api.get('/admin/stats');

export default api;
