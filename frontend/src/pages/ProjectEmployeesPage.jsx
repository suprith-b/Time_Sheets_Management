import React, { useState, useEffect } from 'react';
import {
  Container,
  Title,
  TextInput,
  Button,
  Group,
  Stack,
  Grid,
  Alert,
  Paper,
  ScrollArea,
  Text,
} from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { userService } from '../services/userService';

const ProjectEmployeesPage = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [msg, setMsg] = useState('');

  const [assignedUsers, setAssignedUsers] = useState([]);
  const [unassignedUsers, setUnassignedUsers] = useState([]);
  const [usersToDeassign, setUsersToDeassign] = useState([]);
  const [usersToAssign, setUsersToAssign] = useState([]);

  const [assignedSearch, setAssignedSearch] = useState('');
  const [unassignedSearch, setUnassignedSearch] = useState('');

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const [assigned, unassigned] = await Promise.all([
          userService.fetchUsers({ projectIds: [Number(projectId)] }),
          userService.getProjectUnassignedUsers(Number(projectId)),
        ]);
        setAssignedUsers(assigned);
        setUnassignedUsers(unassigned);
      } catch (err) {
        console.error('Failed to load users:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [projectId]);

  const toggleDeassign = (userId) => {
    setUsersToDeassign((prev) =>
      prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
    );
  };

  const toggleAssign = (userId) => {
    setUsersToAssign((prev) =>
      prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
    );
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setMsg('');
    try {
      if (usersToAssign.length > 0) {
        await projectService.addUsersToProject(Number(projectId), usersToAssign);
      }
      if (usersToDeassign.length > 0) {
        await projectService.revokeUsersFromProject(Number(projectId), usersToDeassign);
      }
      setMsg('Changes saved successfully');
      const [assigned, unassigned] = await Promise.all([
        userService.fetchUsers({ projectIds: [Number(projectId)] }),
        userService.getProjectUnassignedUsers(Number(projectId)),
      ]);
      setAssignedUsers(assigned);
      setUnassignedUsers(unassigned);
      setUsersToDeassign([]);
      setUsersToAssign([]);
    } catch (err) {
      setMsg('Failed to save changes');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const filteredAssigned = assignedUsers.filter(
    (u) =>
      u.name.toLowerCase().includes(assignedSearch.toLowerCase()) ||
      (u.userid && u.userid.toLowerCase().includes(assignedSearch.toLowerCase()))
  );

  const filteredUnassigned = unassignedUsers.filter(
    (u) =>
      u.name.toLowerCase().includes(unassignedSearch.toLowerCase()) ||
      (u.userid && u.userid.toLowerCase().includes(unassignedSearch.toLowerCase()))
  );

  if (loading) {
    return (
      <Container size="lg" py="xl">
        <Title order={3}>Loading...</Title>
      </Container>
    );
  }

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" mb="lg">
        <Title order={2}>Manage Employees</Title>
        <Button variant="default" onClick={() => navigate(`/projects/${projectId}`)}>
          Back to Project
        </Button>
      </Group>

      {msg && (
        <Alert color="blue" mb="md">
          {msg}
        </Alert>
      )}

      <Grid>
        <Grid.Col span={6}>
          <Paper p="md" withBorder>
            <Title order={4} mb="md">
              Assigned
            </Title>
            <TextInput
              placeholder="Search assigned..."
              leftSection={<IconSearch size={16} />}
              value={assignedSearch}
              onChange={(e) => setAssignedSearch(e.target.value)}
              mb="md"
            />
            <ScrollArea h={400}>
              <Stack gap="xs">
                {filteredAssigned.length > 0 ? (
                  filteredAssigned.map((user) => (
                    <Button
                      key={user.id}
                      color={usersToDeassign.includes(user.id) ? 'red' : 'green'}
                      variant="light"
                      onClick={() => toggleDeassign(user.id)}
                      fullWidth
                      justify="flex-start"
                    >
                      {user.name} ({user.userid || user.id})
                    </Button>
                  ))
                ) : (
                  <Text size="sm" c="dimmed" align="center">
                    No assigned employees match search
                  </Text>
                )}
              </Stack>
            </ScrollArea>
          </Paper>
        </Grid.Col>

        <Grid.Col span={6}>
          <Paper p="md" withBorder>
            <Title order={4} mb="md">
              Unassigned
            </Title>
            <TextInput
              placeholder="Search unassigned..."
              leftSection={<IconSearch size={16} />}
              value={unassignedSearch}
              onChange={(e) => setUnassignedSearch(e.target.value)}
              mb="md"
            />
            <ScrollArea h={400}>
              <Stack gap="xs">
                {filteredUnassigned.length > 0 ? (
                  filteredUnassigned.map((user) => (
                    <Button
                      key={user.id}
                      color={usersToAssign.includes(user.id) ? 'green' : 'red'}
                      variant="light"
                      onClick={() => toggleAssign(user.id)}
                      fullWidth
                      size = "sm"
                      justify="flex-start"
                    >
                      {user.name} ({user.userid || user.id})
                    </Button>
                  ))
                ) : (
                  <Text size="sm" c="dimmed" align="center">
                    No unassigned employees match search
                  </Text>
                )}
              </Stack>
            </ScrollArea>
          </Paper>
        </Grid.Col>
      </Grid>

      <Group justify="flex-end" mt="lg">
        <Button variant="default" onClick={() => navigate(`/projects/${projectId}`)}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          loading={submitting}
          disabled={usersToAssign.length === 0 && usersToDeassign.length === 0}
        >
          Save Changes
        </Button>
      </Group>
    </Container>
  );
};

export default ProjectEmployeesPage;
