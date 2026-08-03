import React, { useState } from 'react';
import { Paper, Title, TextInput, Checkbox, Stack, Group, Text, ScrollArea } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { projectService } from '../services/projectService';

const ProjectMembersSection = ({
  projectId,
  allEmployees = [],
  assignedUserIds = [],
  canManage,
  onMembersUpdated,
}) => {
  const [search, setSearch] = useState('');
  const [loadingUserId, setLoadingUserId] = useState(null);

  const filteredEmployees = allEmployees.filter(
    (e) =>
      e.name.toLowerCase().includes(search.toLowerCase()) ||
      (e.userid && e.userid.toLowerCase().includes(search.toLowerCase()))
  );

  const handleToggle = async (user, isAssigned) => {
    setLoadingUserId(user.id);
    try {
      if (isAssigned) {
        // Revoke
        await projectService.revokeUsersFromProject(projectId, [user.id]);
      } else {
        // Add
        await projectService.addUsersToProject(projectId, [user.id]);
      }
      if (onMembersUpdated) onMembersUpdated();
    } catch (err) {
      console.error('Failed to update project member:', err);
    } finally {
      setLoadingUserId(null);
    }
  };

  return (
    <Paper p="md" withBorder mt="md">
      <Group justify="space-between" mb="md">
        <Title order={4}>Assigned Employees</Title>
        <TextInput
          placeholder="Search employees..."
          leftSection={<IconSearch size={16} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Group>

      <ScrollArea h={220}>
        <Stack gap="xs">
          {filteredEmployees.length > 0 ? (
            filteredEmployees.map((emp) => {
              const isChecked = assignedUserIds.includes(emp.id);
              return (
                <Paper key={emp.id} p="xs" withBorder bg={isChecked ? 'blue.0' : 'gray.0'}>
                  <Group justify="space-between">
                    <div>
                      <Text fw={500} size="sm">
                        {emp.name} ({emp.userid || emp.id})
                      </Text>
                      <Text size="xs" c="dimmed">
                        {emp.company_mail} | Roles: {emp.roles?.join(', ')}
                      </Text>
                    </div>

                    <Checkbox
                      checked={isChecked}
                      disabled={!canManage || loadingUserId === emp.id}
                      onChange={() => handleToggle(emp, isChecked)}
                      label={isChecked ? 'Assigned' : 'Unassigned'}
                    />
                  </Group>
                </Paper>
              );
            })
          ) : (
            <Text size="sm" c="dimmed" align="center">
              No employees match search
            </Text>
          )}
        </Stack>
      </ScrollArea>
    </Paper>
  );
};

export default ProjectMembersSection;
