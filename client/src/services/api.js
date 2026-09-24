import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const TOKEN_KEY = 'ra_token';

export const auth = {
  getToken: () => localStorage.getItem(TOKEN_KEY),
  setToken: (t) => localStorage.setItem(TOKEN_KEY, t),
  clear: () => localStorage.removeItem(TOKEN_KEY),
};

const client = axios.create({ baseURL: API_URL });
client.interceptors.request.use((config) => {
  const token = auth.getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const api = {
  signup: async ({ email, password, name }) => {
    const { data } = await client.post('/api/auth/signup', { email, password, name });
    auth.setToken(data.token);
    return data.user;
  },

  login: async ({ email, password }) => {
    const { data } = await client.post('/api/auth/login', { email, password });
    auth.setToken(data.token);
    return data.user;
  },

  // Restores the session after a page refresh; resolves null if there is no valid token.
  me: async () => {
    if (!auth.getToken()) return null;
    try {
      const { data } = await client.get('/api/auth/me');
      return data.user;
    } catch {
      auth.clear();
      return null;
    }
  },

  logout: () => auth.clear(),

  analyzeResume: async ({ resumeFile, resumeText, jobDescription }) => {
    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);
      if (resumeFile) {
        formData.append('resume_file', resumeFile);
      } else {
        formData.append('resume_text', resumeText);
      }

      const response = await client.post('/api/analyze', formData);
      return response.data;
    } catch (error) {
      console.error("API Error:", error);
      if (error.response?.status === 401) auth.clear();
      throw error;
    }
  }
};
