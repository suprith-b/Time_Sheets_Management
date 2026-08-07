import React, { useState, useEffect } from 'react';
import {
  Paper,
  TextInput,
  MultiSelect,
  Select,
  Button,
  Group,
  Stack,
  Text,
  Badge,
  Grid,
  Box,
} from '@mantine/core';
import { useAuth } from './AuthContext';
import { RoleEnum, ROLE_OPTIONS } from '../utils/constants';
import { userService } from '../services/userService';
import PasswordChangeForm from './PasswordChangeForm';

const STATUS_SELECT_OPTIONS = [
  { value: '1', label: 'Active' },
  { value: '0', label: 'Inactive' },
];

const ProfileDetailsSection = ({
  targetUser,
  userProjects = [],
  managersList = [],
  onUpdateSuccess,
}) => {
  const { user: currentUser, hasRole } = useAuth();
  const isAdmin = hasRole(RoleEnum.ADMIN);
  const isSelf = currentUser?.id === targetUser?.id;

  const [formData, setFormData] = useState({
    name: '',
    username: '',
    userid: '',
    company_mail: '',
    phone_number: '',
    manager_id: null,
    roles: [],
    is_alive: 1,
  });

  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState({ type: '', text: '' });

  useEffect(() => {
    if (targetUser) {
      setFormData({
        name: targetUser.name || '',
        username: targetUser.username || '',
        userid: targetUser.userid || '',
        company_mail: targetUser.company_mail || '',
        phone_number: targetUser.phone_number || '',
        manager_id: targetUser.manager_id || null,
        roles: targetUser.roles || [],
        is_alive: targetUser.is_alive ?? 1,
      });
    }
  }, [targetUser]);

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setLoading(true);
    setMsg({ type: '', text: '' });
    try {
      await userService.updateUser(targetUser.id, {
        name: formData.name,
        username: formData.username,
        userid: formData.userid,
        company_mail: formData.company_mail,
        phone_number: formData.phone_number,
        manager_id: formData.manager_id,
        roles: formData.roles,
        is_alive: formData.is_alive,
      });
      setMsg({ type: 'success', text: 'Details updated successfully' });
      if (onUpdateSuccess) onUpdateSuccess();
    } catch (err) {
      setMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to update user details',
      });
    } finally {
      setLoading(false);
    }
  };

  const managerOptions = managersList.map((m) => ({
    value: String(m.id),
    label: `${m.name} (${m.userid || m.id})`,
  }));

  return (
    <Stack gap="md">
      <Paper p="md" withBorder>
        <Grid>
          <Grid.Col span={6}>
            <TextInput
              label="User ID"
              value={formData.userid}
              onChange={(e) => handleChange('userid', e.target.value)}
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <TextInput
              label="Name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <TextInput
              label="Username"
              value={formData.username}
              onChange={(e) => handleChange('username', e.target.value)}
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <TextInput
              label="Company Email"
              value={formData.company_mail}
              onChange={(e) => handleChange('company_mail', e.target.value)}
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <TextInput
              label="Phone Number"
              value={formData.phone_number}
              onChange={(e) => handleChange('phone_number', e.target.value)}
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <Select
              label="Manager"
              placeholder="None"
              data={managerOptions}
              value={formData.manager_id ? String(formData.manager_id) : null}
              onChange={(val) => handleChange('manager_id', val ? Number(val) : null)}
              searchable
              clearable
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <MultiSelect
              label="Roles"
              data={ROLE_OPTIONS}
              value={formData.roles}
              onChange={(val) => handleChange('roles', val)}
              disabled={!isAdmin}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <Select
              label="Status"
              data={STATUS_SELECT_OPTIONS}
              value={String(formData.is_alive)}
              onChange={(val) => handleChange('is_alive', Number(val))}
              disabled={!isAdmin}
            />
          </Grid.Col>
        </Grid>

        <Box mt="md">
          <Text fw={500} size="sm" mb={4}>
            Assigned Projects
          </Text>
          <Group gap="xs">
            {userProjects.length > 0 ? (
              userProjects.map((p) => (
                <Badge key={p.id} variant="light" color="cyan">
                  {p.name}
                </Badge>
              ))
            ) : (
              <Text size="sm" c="dimmed">
                No projects assigned
              </Text>
            )}
          </Group>
        </Box>

        {isAdmin && (
          <Group justify="flex-end" mt="md">
            <Button onClick={handleSave} loading={loading}>
              Save Details
            </Button>
          </Group>
        )}

        {msg.text && (
          <Text color={msg.type === 'success' ? 'green' : 'red'} size="sm" mt="xs">
            {msg.text}
          </Text>
        )}
      </Paper>

      {isSelf && <PasswordChangeForm userId={targetUser.id} />}
    </Stack>
  );
};

export default ProfileDetailsSection;
