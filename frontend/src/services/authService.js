import { authApi } from '../apis/authApi';

export const authService = {
  login: async (company_mail, password) => {
    return await authApi.login({ company_mail, password });
  },

  refresh: async () => {
    return await authApi.refresh();
  },

  logout: async () => {
    return await authApi.logout();
  },
};
