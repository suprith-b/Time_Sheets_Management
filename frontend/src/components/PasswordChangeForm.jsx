import React, { useState } from 'react';
import { Paper, Title, PasswordInput, Button, Group, Text } from '@mantine/core';
import { userService } from '../services/userService';

const PasswordChangeForm = ({ userId }) => {
  const [editing, setEditing] = useState(false);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSave = async () => {
    if (!newPassword || newPassword.trim() === '') {
      setError('Password cannot be empty');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    try {
      await userService.updatePassword(userId, newPassword);
      setMessage('Password updated successfully');
      setNewPassword('');
      setConfirmPassword('');
      setEditing(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper p="md" withBorder mt="md">
      <Title order={5} mb="xs">
        Password Security
      </Title>

      {!editing ? (
        <Group justify="space-between">
          <Text c="dimmed">Password: ••••••••</Text>
          <Button variant="outline" size="xs" onClick={() => setEditing(true)}>
            Change Password
          </Button>
        </Group>
      ) : (
        <Group align="flex-end" grow>
          <PasswordInput
            label="New Password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <PasswordInput
            label="Confirm Password"
            placeholder="Confirm new password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <Group gap="xs">
            <Button size="xs" onClick={handleSave} loading={loading}>
              Save
            </Button>

            <Button
              size="xs"
              variant="default"
              onClick={() => {
                setEditing(false);
                setError('');
              }}
            >
              Cancel
            </Button>
          </Group>
        </Group>
      )}

      {error && (
        <Text color="red" size="sm" mt="xs">
          {error}
        </Text>
      )}
      {message && (
        <Text color="green" size="sm" mt="xs">
          {message}
        </Text>
      )}
    </Paper>
  );
};

export default PasswordChangeForm;
