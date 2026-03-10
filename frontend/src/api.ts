import axios from 'axios';

// Get backend URL from env, or default to localhost for local testing
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface UserCreate {
  name: string;
  email: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
}

export const userApi = {
  getUsers: async () => {
    const response = await apiClient.get<User[]>('/users');
    return response.data;
  },
  getUser: async (id: string) => {
    const response = await apiClient.get<User>(`/users/${id}`);
    return response.data;
  },
  createUser: async (user: UserCreate) => {
    const response = await apiClient.post<User>('/users', user);
    return response.data;
  },
  updateUser: async (id: string, user: UserUpdate) => {
    const response = await apiClient.put<User>(`/users/${id}`, user);
    return response.data;
  },
  deleteUser: async (id: string) => {
    await apiClient.delete(`/users/${id}`);
  },
};
