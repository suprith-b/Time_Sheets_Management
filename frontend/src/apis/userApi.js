import axiosClient from './axiosClient';

export const userApi = {
  // ---- Auth ----
  login: async (credentials) => {
    const response = await axiosClient.post('/auth/login', credentials);
    return response.data; // returns { id, userid, username, name, roles }
  },

  logout: async () => {
    const response = await axiosClient.post('/auth/logout');
    return response.data;
  },

  // ---- User CRUD ----
  getUsers: async (params) => {
    const response = await axiosClient.get('/users', { params });
    return response.data;
  },

  getUserById: async (userId) => {
    const response = await axiosClient.get(`/users/${userId}`);
    return response.data;
  },

  createUser: async (data) => {
    const response = await axiosClient.post('/users', data);
    return response.data;
  },

  editUser: async (userId, data) => {
    const response = await axiosClient.patch(`/users/${userId}`, data);
    return response.data;
  },

  updatePassword: async (userId, data) => {
    // Backend endpoint: PATCH /users/password/{user_id}
    const response = await axiosClient.patch(`/users/password/${userId}`, data);
    return response.data;
  },
};
