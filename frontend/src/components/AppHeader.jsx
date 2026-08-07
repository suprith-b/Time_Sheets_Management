import React from 'react';
import { Group, Button, Title, Badge, Box, Text, Avatar, Menu, UnstyledButton } from '@mantine/core';
import { IconLogout, IconUser, IconClock } from '@tabler/icons-react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { ROLE_OPTIONS, RoleEnum } from '../utils/constants';

const AppHeader = () => {
  const { user, logout, isOneOfRoles } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  if (!user) return null;

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const initials = user.name
    ? user.name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2)
    : '?';

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
            onClick={() => navigate('/timesheet')}
          >
            Timesheets
          </Title>
          <Group gap="xs">
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
            {isOneOfRoles( [ RoleEnum.EMPLOYEE ] ) && (
              <Button
                variant={location.pathname === '/timelogs' ? 'filled' : 'subtle'}
                size="sm"
                onClick={() => navigate('/timelogs')}
              >
                Timelogs
              </Button>
            )}
          </Group>
        </Group>

        <Group gap="sm" align="center">
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
          <Menu shadow="md" width={180} position="bottom-end">
            <Menu.Target>
              <UnstyledButton style={{ display: 'flex', alignItems: 'center' }}>
                <Avatar
                  radius="xl"
                  size="sm"
                  color="blue"
                  style={{ cursor: 'pointer' }}
                >
                  {initials}
                </Avatar>
              </UnstyledButton>
            </Menu.Target>
            <Menu.Dropdown>
              <Menu.Item
                leftSection={<IconUser size={14} />}
                onClick={() => navigate('/profile')}
              >
                My Profile
              </Menu.Item>
              <Menu.Divider />
              <Menu.Item
                color="red"
                leftSection={<IconLogout size={14} />}
                onClick={handleLogout}
              >
                Logout
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </Group>
      </Group>
    </Box>
  );
};

export default AppHeader;
