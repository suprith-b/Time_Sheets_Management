import React from 'react';
import { Group, Button, Title, Badge, Box, Text, Avatar, Menu, UnstyledButton, Container } from '@mantine/core';
import { IconLogout, IconUser, IconClock, IconBriefcase, IconUsers, IconChartBar, IconCalendar } from '@tabler/icons-react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { RoleEnum } from '../utils/constants';

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
        borderBottom: '1px solid #e2e8f0',
        padding: '14px 0',
        backgroundColor: '#ffffff',
        boxShadow: '0 1px 3px 0 rgba(15, 23, 42, 0.05)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
    >
      <Container size="lg">
        <Group justify="space-between" align="center">
          <Group gap="xl">
            <Group gap="xs" style={{ cursor: 'pointer' }} onClick={() => navigate('/timesheet')}>
              <Box
                style={{
                  width: 36,
                  height: 36,
                  borderRadius: 10,
                  background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#ffffff',
                  boxShadow: '0 2px 8px rgba(79, 70, 229, 0.3)',
                }}
              >
                <IconClock size={20} />
              </Box>
              <Title order={3} style={{ fontSize: '1.25rem', fontWeight: 700, color: '#0f172a' }}>
                TimeSheets
              </Title>
            </Group>

            <Group gap="xs">
              {isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]) && (
                <Button
                  variant={location.pathname.startsWith('/employees') ? 'filled' : 'subtle'}
                  color={location.pathname.startsWith('/employees') ? 'indigo' : 'gray'}
                  size="sm"
                  radius="xl"
                  leftSection={<IconUsers size={16} />}
                  onClick={() => navigate('/employees')}
                >
                  Employees
                </Button>
              )}
              <Button
                variant={location.pathname.startsWith('/projects') ? 'filled' : 'subtle'}
                color={location.pathname.startsWith('/projects') ? 'indigo' : 'gray'}
                size="sm"
                radius="xl"
                leftSection={<IconBriefcase size={16} />}
                onClick={() => navigate('/projects')}
              >
                Projects
              </Button>
              {isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]) && (
                <Button
                  variant={location.pathname === '/reports' ? 'filled' : 'subtle'}
                  color={location.pathname === '/reports' ? 'indigo' : 'gray'}
                  size="sm"
                  radius="xl"
                  leftSection={<IconChartBar size={16} />}
                  onClick={() => navigate('/reports')}
                >
                  Reports
                </Button>
              )}
              {isOneOfRoles([RoleEnum.EMPLOYEE, RoleEnum.ADMIN]) && (
                <Button
                  variant={location.pathname === '/timesheet' ? 'filled' : 'subtle'}
                  color={location.pathname === '/timesheet' ? 'indigo' : 'gray'}
                  size="sm"
                  radius="xl"
                  leftSection={<IconCalendar size={16} />}
                  onClick={() => navigate('/timesheet')}
                >
                  Timesheet
                </Button>
              )}
              {isOneOfRoles([RoleEnum.EMPLOYEE]) && (
                <Button
                  variant={location.pathname === '/timelogs' ? 'filled' : 'subtle'}
                  color={location.pathname === '/timelogs' ? 'indigo' : 'gray'}
                  size="sm"
                  radius="xl"
                  leftSection={<IconClock size={16} />}
                  onClick={() => navigate('/timelogs')}
                >
                  Timelogs
                </Button>
              )}
            </Group>
          </Group>

          <Group gap="md" align="center">
            <Box style={{ textAlign: 'right' }}>
              <Text size="sm" fw={600} c="dark">
                {user.name}
              </Text>
              <Group gap={4} justify="flex-end" mt={2}>
                {user.roles?.map((r) => (
                  <Badge key={r} size="xs" variant="light" color="indigo" radius="xl">
                    {r}
                  </Badge>
                ))}
              </Group>
            </Box>
            <Menu shadow="md" width={180} position="bottom-end" radius="md">
              <Menu.Target>
                <UnstyledButton style={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar
                    radius="xl"
                    size="md"
                    color="indigo"
                    style={{ cursor: 'pointer', border: '2px solid #818cf8' }}
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
      </Container>
    </Box>
  );
};

export default AppHeader;
