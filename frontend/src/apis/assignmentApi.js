import axiosClient from './axiosClient';

export const assignmentApi = {
  addRolesToUsers: async (data) => {
    const response = await axiosClient.post('/assignments/roles/add', data);
    return response.data;
  },

  revokeRolesFromUsers: async (data) => {
    const response = await axiosClient.patch('/assignments/roles/revoke', data);
    return response.data;
  },

  updateManagerForUsers: async (managerId, data) => {
    const response = await axiosClient.patch(`/assignments/manager/${managerId}`, data);
    return response.data;
  },

  addProjectsToUser: async (userId, data) => {
    const response = await axiosClient.post(`/assignments/projects/add/to/user/${userId}`, data);
    return response.data;
  },

  revokeProjectsFromUser: async (userId, data) => {
    const response = await axiosClient.post(`/assignments/projects/revoke/from/user/${userId}`, data);
    return response.data;
  },

  addUsersToProject: async (projectId, data) => {
    const response = await axiosClient.post(`/assignments/users/add/to/project/${projectId}`, data);
    return response.data;
  },

  revokeUsersFromProject: async (projectId, data) => {
    const response = await axiosClient.post(`/assignments/users/revoke/from/project/${projectId}`, data);
    return response.data;
  },
};
