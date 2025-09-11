import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
export const api = axios.create({ baseURL, timeout: 20000 });

api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API error:", err?.response?.status, err?.response?.data || err.message);
    return Promise.reject(err);
  }
);

export default api;
