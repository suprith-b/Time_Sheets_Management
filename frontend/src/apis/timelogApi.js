import axiosClient from './axiosClient';

export const timelogApi = {
  createTimeLogs: async (userId, data) => {
    const response = await axiosClient.post(`/timelogs/${userId}`, data);
    return response.data;
  },

  getUserTimeLogs: async (userId, params) => {
    const response = await axiosClient.get(`/timelogs/${userId}`, { params });
    return response.data;
  },

  getUserTimeLogHours: async (userId, params) => {
    const response = await axiosClient.get(`/timelogs/hours/${userId}`, { params });
    return response.data;
  },

  updateTimeLog: async (timelogId, data) => {
    const response = await axiosClient.patch(`/timelogs/${timelogId}`, data);
    return response.data;
  },
};
