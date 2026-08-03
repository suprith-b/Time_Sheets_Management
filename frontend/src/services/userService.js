import { userApi } from '../apis/userApi';
import { assignmentApi } from '../apis/assignmentApi';

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

  getUserById: async (userId) => {
    return await userApi.getUserById(userId);
  },

  createUser: async (userData) => {
    return await userApi.createUser(userData);
  },

  updateUser: async (userId, userData) => {
    return await userApi.editUser(userId, userData);
  },

  updatePassword: async (userId, newPassword) => {
    return await userApi.updatePassword(userId, { password: newPassword });
  },

  toggleUserStatus: async (userId, currentIsAlive) => {
    const nextStatus = currentIsAlive === 1 ? 0 : 1;
    return await userApi.editUser(userId, { is_alive: nextStatus });
  },

  assignManager: async (managerId, userIds) => {
    return await assignmentApi.updateManagerForUsers(managerId, { users: userIds });
  },
};
