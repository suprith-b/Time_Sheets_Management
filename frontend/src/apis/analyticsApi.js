import axiosClient from './axiosClient';

export const analyticsApi = {
  getReports: async (params) => {
    const response = await axiosClient.get('/analytics/reports', { params });
    return response.data;
  },
};
