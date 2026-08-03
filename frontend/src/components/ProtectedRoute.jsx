import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Center, Loader } from '@mantine/core';
import { useAuth } from './AuthContext';

const ProtectedRoute = ({ allowedRoles = [] }) => {
  const { user, loading, isOneOfRoles } = useAuth();

  if (loading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles.length > 0 && !isOneOfRoles(allowedRoles)) {
    return <Navigate to="/profile" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
