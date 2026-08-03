import { projectApi } from '../apis/projectApi';
import { taskApi } from '../apis/taskApi';
import { assignmentApi } from '../apis/assignmentApi';

export const projectService = {
  fetchProjects: async (filters = {}) => {
    const params = {
      sort_by: filters.sortBy || 'duration',
      sort_type: filters.sortType || -1,
    };
    if (filters.status && filters.status.length > 0) {
      params.status = filters.status;
    }
    return await projectApi.getProjects(params);
  },

  fetchUserProjects: async (userId, filters = {}) => {
    const params = {
      sort_by: filters.sortBy || 'duration',
      sort_type: filters.sortType || -1,
    };
    if (filters.status && filters.status.length > 0) {
      params.status = filters.status;
    }
    return await projectApi.getUserProjects(userId, params);
  },

  getProjectById: async (projectId) => {
    return await projectApi.getProjectById(projectId);
  },

  createProject: async (projectData) => {
    return await projectApi.createProject(projectData);
  },

  updateProject: async (projectId, updateData) => {
    return await projectApi.updateProject(projectId, updateData);
  },

  fetchTasks: async (projectId) => {
    return await taskApi.getTasks(projectId);
  },

  createTask: async (projectId, taskData) => {
    return await taskApi.createTask(projectId, taskData);
  },

  updateTask: async (taskId, taskData) => {
    return await taskApi.updateTask(taskId, taskData);
  },

  deleteTask: async (taskId) => {
    return await taskApi.deleteTask(taskId);
  },

  addUsersToProject: async (projectId, userIds) => {
    return await assignmentApi.addUsersToProject(projectId, { users: userIds });
  },

  revokeUsersFromProject: async (projectId, userIds) => {
    return await assignmentApi.revokeUsersFromProject(projectId, { users: userIds });
  },
};
