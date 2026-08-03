import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Title,
  TextInput,
  NumberInput,
  Select,
  Button,
  Group,
  Stack,
  Grid,
  Alert,
} from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import { RoleEnum, STATUS_OPTIONS } from '../utils/constants';
import { projectService } from '../services/projectService';
import { userService } from '../services/userService';
import ProjectTasksSection from '../components/ProjectTasksSection';
import ProjectMembersSection from '../components/ProjectMembersSection';

const ProjectDetailPage = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const { hasRole, isOneOfRoles } = useAuth();

  const isAdmin = hasRole(RoleEnum.ADMIN);
  const isManager = hasRole(RoleEnum.MANAGER);
  const canManage = isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]);

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [allEmployees, setAllEmployees] = useState([]);
  const [assignedUserIds, setAssignedUserIds] = useState([]);

  const [formData, setFormData] = useState({
    name: '',
    duration: 0,
    start_date: null,
    end_date: null,
    status: '',
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const pData = await projectService.getProjectById(Number(projectId));
      setProject(pData);
      setFormData({
        name: pData.name || '',
        duration: pData.duration || 0,
        start_date: pData.start_date ? new Date(pData.start_date) : null,
        end_date: pData.end_date ? new Date(pData.end_date) : null,
        status: pData.status || '',
      });

      const tData = await projectService.fetchTasks(Number(projectId));
      setTasks(tData);

      const empData = await userService.fetchUsers({
        roles: [RoleEnum.EMPLOYEE, RoleEnum.MANAGER, RoleEnum.ADMIN],
        isAlive: [1],
      });
      setAllEmployees(empData);

      const assignedEmps = await userService.fetchUsers({
        projectIds: [Number(projectId)],
      });
      setAssignedUserIds(assignedEmps.map((u) => u.id));
    } catch (err) {
      console.error('Failed to load project details:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [projectId]);

  const handleSaveDetails = async () => {
    setSaving(true);
    setMsg('');
    try {
      await projectService.updateProject(Number(projectId), {
        name: formData.name,
        duration: formData.duration,
        start_date: formData.start_date
          ? formData.start_date.toISOString().split('T')[0]
          : null,
        end_date: formData.end_date
          ? formData.end_date.toISOString().split('T')[0]
          : null,
        status: formData.status,
      });
      setMsg('Project details saved successfully');
      loadData();
    } catch (err) {
      setMsg('Failed to save project details');
    } finally {
      setSaving(false);
    }
  };

  if (loading || !project) {
    return (
      <Container size="lg" py="xl">
        <Title order={3}>Loading project...</Title>
      </Container>
    );
  }

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" mb="lg">
        <Title order={2}>Project: {project.name}</Title>
        <Button variant="default" onClick={() => navigate('/projects')}>
          Back to Projects
        </Button>
      </Group>

      {msg && (
        <Alert color="blue" mb="md">
          {msg}
        </Alert>
      )}

      <Paper p="md" withBorder>
        <Grid>
          <Grid.Col span={6}>
            <TextInput
              label="Project Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              disabled={!canManage}
            />
          </Grid.Col>

          <Grid.Col span={6}>
            <Select
              label="Status"
              data={STATUS_OPTIONS}
              value={formData.status}
              onChange={(val) => setFormData({ ...formData, status: val })}
              disabled={!canManage}
            />
          </Grid.Col>

          <Grid.Col span={4}>
            <NumberInput
              label="Duration (days)"
              value={formData.duration}
              onChange={(val) => setFormData({ ...formData, duration: Number(val) })}
              disabled={!canManage}
            />
          </Grid.Col>

          <Grid.Col span={4}>
            <DateInput
              label="Start Date"
              value={formData.start_date}
              onChange={(val) => setFormData({ ...formData, start_date: val })}
              disabled={!canManage}
            />
          </Grid.Col>

          <Grid.Col span={4}>
            <DateInput
              label="End Date"
              value={formData.end_date}
              onChange={(val) => setFormData({ ...formData, end_date: val })}
              disabled
            />
          </Grid.Col>
        </Grid>

        {canManage && (
          <Group justify="flex-end" mt="md">
            <Button onClick={handleSaveDetails} loading={saving}>
              Save Details
            </Button>
          </Group>
        )}
      </Paper>

      <ProjectTasksSection
        projectId={Number(projectId)}
        tasks={tasks}
        canManage={canManage}
        onTasksUpdated={loadData}
      />

      <ProjectMembersSection
        projectId={Number(projectId)}
        allEmployees={allEmployees}
        assignedUserIds={assignedUserIds}
        canManage={canManage}
        onMembersUpdated={loadData}
      />
    </Container>
  );
};

export default ProjectDetailPage;
