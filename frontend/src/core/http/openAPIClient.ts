import axios from "axios";
import { HealthApi } from "../api/api";
import { Configuration } from "../api/configuration";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/";

const configuration = new Configuration({
  basePath: API_BASE_URL,
});

export const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

axiosInstance.interceptors.request.use((config) => {
  // TODO: Add token to headers if available
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => {
    // TODO: Handle successful responses
    return response;
  },
  (error) => {
    // TODO: Handle errors globally
    return Promise.reject(error);
  },
);

const healthApi = new HealthApi(configuration, "", axiosInstance);

export { healthApi };
