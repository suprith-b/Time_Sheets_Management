import axiosClient from './axiosClient';

export const projectApi = {
  getProjects: async (params) => {
    const response = await axiosClient.get('/projects', { params });
    return response.data;
  },

  getUserProjects: async (userId, params) => {
    const response = await axiosClient.get(`/projects/user/${userId}`, { params });
    return response.data;
  },

  getProjectById: async (projectId) => {
    const response = await axiosClient.get(`/projects/${projectId}`);
    return response.data;
  },

  createProject: async (data) => {
    const response = await axiosClient.post('/projects', data);
    return response.data;
  },

  updateProject: async (projectId, data) => {
    const response = await axiosClient.patch(`/projects/${projectId}`, data);
    return response.data;
  },

  deleteProject: async (projectId) => {
    const response = await axiosClient.delete(`/projects/${projectId}`);
    return response.data;
  },

  getProjectUnassignedUsers: async (projectId) => {
    const response = await axiosClient.get(`/projects/${projectId}/unassigned/users`);
    return response.data;
  },
};
