import axiosClient from './axiosClient';

export const taskApi = {
  getTasks: async (projectId, params) => {
    const response = await axiosClient.get(`/tasks/${projectId}`, { params });
    return response.data;
  },

  createTask: async (projectId, data) => {
    const response = await axiosClient.post(`/tasks/${projectId}`, data);
    return response.data;
  },

  updateTask: async (taskId, data) => {
    const response = await axiosClient.patch(`/tasks/${taskId}`, data);
    return response.data;
  },

  deleteTask: async (taskId) => {
    const response = await axiosClient.delete(`/tasks/${taskId}`);
    return response.data;
  },
};
