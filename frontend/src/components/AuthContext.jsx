import React, { createContext, useContext, useEffect, useState } from 'react';
import { RoleEnum } from '../utils/constants';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On mount, refresh token to retrieve current user details into memory
  useEffect(() => {
    let isMounted = true;
    authService
      .refresh()
      .then((userData) => {
        if (isMounted) {
          setUser(userData);
        }
      })
      .catch(() => {
        if (isMounted) {
          setUser(null);
        }
      })
      .finally(() => {
        if (isMounted) {
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    setUser(data);
    return data;
  };

  const logout = async () => {
    try {
      await authService.logout();
    } finally {
      setUser(null);
    }
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
