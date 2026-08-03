import { timelogApi } from '../apis/timelogApi';

export const timelogService = {
  createTimeLogs: async (userId, timeLogs) => {
    return await timelogApi.createTimeLogs(userId, { time_logs: timeLogs });
  },

  getUserTimeLogs: async (userId, filters = {}) => {
    const params = {
      sort_by: filters.sortBy || 'start_time',
      sort_type: filters.sortType || -1,
    };
    if (filters.projectIds && filters.projectIds.length > 0) {
      params.project_ids = filters.projectIds;
    }
    if (filters.startDate) {
      params.start_date = filters.startDate;
    }
    if (filters.endDate) {
      params.end_date = filters.endDate;
    }
    if (filters.type && filters.type.length > 0) {
      params.type = filters.type;
    }
    return await timelogApi.getUserTimeLogs(userId, params);
  },

  getUserHours: async (userId, filters = {}) => {
    const params = {};
    if (filters.startDate) params.start_date = filters.startDate;
    if (filters.endDate) params.end_date = filters.endDate;
    if (filters.type) params.type = filters.type;
    return await timelogApi.getUserTimeLogHours(userId, params);
  },
};
