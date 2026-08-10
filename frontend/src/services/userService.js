import { userApi } from '../apis/userApi';
import { assignmentApi } from '../apis/assignmentApi';
import { projectApi } from '../apis/projectApi';

export const userService = {
  fetchUsers: async (filters = {}) => {
    const params = {};
    if (filters.roles && filters.roles.length > 0) {
      params.roles = filters.roles;
    }
    if (filters.managerId) {
      params.manager_id = filters.managerId;
    }
    if (filters.isAlive && filters.isAlive.length > 0) {
      params.is_alive = filters.isAlive;
    }
    if (filters.projectIds && filters.projectIds.length > 0) {
      params.project_ids = filters.projectIds;
    }
    if (filters.hasManager && filters.hasManager.length > 0) {
      params.has_manager = filters.hasManager;
    }
    return await userApi.getUsers(params);
  },


  getManagerByUserId: async (userId) => {
    const user = await userApi.getUserById(userId);
    if (!user || !user.manager_id) return null;
    return await userApi.getUserById(user.manager_id);
  },

  getUserById: async (userId) => {
    return await userApi.getUserById(userId);
  },

  createUser: async (userData) => {
    return await userApi.createUser(userData);
  },

  updateUser: async (userId, userData) => {
    return await userApi.editUser(userId, userData);
  },

  updatePassword: async (userId, oldPassword, newPassword) => {
    return await userApi.updatePassword(userId, { old_password: oldPassword, new_password: newPassword });
  },

  toggleUserStatus: async (userId, currentIsAlive) => {
    const nextStatus = currentIsAlive === 1 ? 0 : 1;
    return await userApi.editUser(userId, { is_alive: nextStatus });
  },

  assignManager: async (managerId, userIds) => {
    return await assignmentApi.updateManagerForUsers(managerId, { users: userIds });
  },
  
  getProjectUnassignedUsers: async (projectId) => {
    return await projectApi.getProjectUnassignedUsers(projectId);
  },
};
