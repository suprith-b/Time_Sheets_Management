import React, { createContext, useContext, useEffect, useState } from 'react';
import { userApi } from '../apis/userApi';
import axiosClient from '../apis/axiosClient';
import { RoleEnum } from '../utils/constants';

const AuthContext = createContext(null);

const USER_KEY = 'ts_user';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem(USER_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);

  // On mount, try to refresh the access token; if it fails the session is expired
  useEffect(() => {
    axiosClient
      .post('/auth/refresh')
      .then(() => {
        // Token still valid – keep stored user
        setLoading(false);
      })
      .catch(() => {
        // No valid session – clear stored user
        localStorage.removeItem(USER_KEY);
        setUser(null);
        setLoading(false);
      });
  }, []);

  const login = async (email, password) => {
    const data = await userApi.login({ company_mail: email, password });
    localStorage.setItem(USER_KEY, JSON.stringify(data));
    setUser(data);
    return data;
  };

  const logout = async () => {
    await userApi.logout();
    localStorage.removeItem(USER_KEY);
    setUser(null);
  };

  // Returns true if the user has any one of the provided roles
  const isOneOfRoles = (allowedRoles) => {
    if (!user?.roles) return false;
    return allowedRoles.some((r) => user.roles.includes(r));
  };

  // Returns true if the user has this specific role
  const hasRole = (role) => {
    if (!user?.roles) return false;
    return user.roles.includes(role);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isOneOfRoles,
    hasRole,
    RoleEnum,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
