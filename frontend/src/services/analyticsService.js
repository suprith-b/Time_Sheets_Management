import { analyticsApi } from '../apis/analyticsApi';

export const analyticsService = {
  getReports: async (filters = {}) => {
    const params = {
      sort_by: filters.sortBy || 'duration',
      sort_type: filters.sortType || -1,
    };
    if (filters.viewAs && filters.viewAs.length > 0) {
      params.view_as = filters.viewAs;
    }
    if (filters.startDate) params.start_date = filters.startDate;
    if (filters.endDate) params.end_date = filters.endDate;
    if (filters.projectIds && filters.projectIds.length > 0) {
      params.project_ids = filters.projectIds;
    }
    if (filters.type && filters.type.length > 0) {
      params.type = filters.type;
    }
    return await analyticsApi.getReports(params);
  },
};
