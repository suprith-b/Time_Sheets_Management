import React from 'react';
import { Group, Button, Title, Badge, Box, Text } from '@mantine/core';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { RoleEnum } from '../utils/constants';

const AppHeader = () => {
  const { user, logout, isOneOfRoles } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  if (!user) return null;

  const isActive = (path) => location.pathname.startsWith(path) && path !== '/profile'
    ? location.pathname.startsWith(path)
    : location.pathname === path;

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <Box
      style={{
        borderBottom: '1px solid var(--mantine-color-gray-3)',
        padding: '10px 24px',
        backgroundColor: 'var(--mantine-color-white)',
      }}
    >
      <Group justify="space-between" align="center">
        <Group gap="md">
          <Title
            order={4}
            style={{ cursor: 'pointer' }}
            onClick={() => navigate('/profile')}
          >
            Timesheets
          </Title>
          <Group gap="xs">
            <Button
              variant={location.pathname === '/profile' ? 'filled' : 'subtle'}
              size="sm"
              onClick={() => navigate('/profile')}
            >
              Profile
            </Button>
            {isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]) && (
              <Button
                variant={location.pathname.startsWith('/employees') ? 'filled' : 'subtle'}
                size="sm"
                onClick={() => navigate('/employees')}
              >
                Employees
              </Button>
            )}
            <Button
              variant={location.pathname.startsWith('/projects') ? 'filled' : 'subtle'}
              size="sm"
              onClick={() => navigate('/projects')}
            >
              Projects
            </Button>
            {isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]) && (
              <Button
                variant={location.pathname === '/reports' ? 'filled' : 'subtle'}
                size="sm"
                onClick={() => navigate('/reports')}
              >
                Reports
              </Button>
            )}
            {isOneOfRoles([RoleEnum.EMPLOYEE, RoleEnum.ADMIN]) && (
              <Button
                variant={location.pathname === '/timesheet' ? 'filled' : 'subtle'}
                size="sm"
                onClick={() => navigate('/timesheet')}
              >
                Timesheet
              </Button>
            )}
          </Group>
        </Group>

        <Group gap="sm">
          <Box style={{ textAlign: 'right' }}>
            <Text size="sm" fw={600}>{user.name}</Text>
            <Group gap={4} justify="flex-end">
              {user.roles?.map((r) => (
                <Badge key={r} size="xs" variant="light" color="blue">
                  {r}
                </Badge>
              ))}
            </Group>
          </Box>
          <Button variant="outline" color="red" size="xs" onClick={handleLogout}>
            Logout
          </Button>
        </Group>
      </Group>
    </Box>
  );
};

export default AppHeader;
