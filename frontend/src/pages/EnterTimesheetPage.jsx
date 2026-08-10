import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Title,
  Button,
  Group,
  Stack,
  Alert,
  Text,
  Select,
} from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import TimesheetRow from '../components/TimesheetRow';
import { projectService } from '../services/projectService';
import { timelogService } from '../services/timelogService';
import { userService } from '../services/userService';
import { TypeEnum, RoleEnum } from '../utils/constants';

const createEmptyRow = () => ({
  project_id: null,
  task_id: null,
  start_time: null,
  end_time: null,
  type: TypeEnum.STANDARD,
  comments: '',
});

const EnterTimesheetPage = () => {
  const navigate = useNavigate();
  const { user, isOneOfRoles } = useAuth();
  const isAdmin = isOneOfRoles([RoleEnum.ADMIN]);

  const [selectedUserId, setSelectedUserId] = useState(null);
  const [employeesList, setEmployeesList] = useState([]);
  const [rows, setRows] = useState([createEmptyRow()]);
  const [userProjects, setUserProjects] = useState([]);
  const [manager, setManager] = useState(null);
  const [tasksMap, setTasksMap] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Set default selectedUserId to logged-in user ID
  useEffect(() => {
    if (user && !selectedUserId) {
      setSelectedUserId(user.id);
    }
  }, [user]);

  // If Admin, fetch all users with EMPLOYEE role
  useEffect(() => {
    if (isAdmin) {
      userService
        .fetchUsers({ roles: [RoleEnum.EMPLOYEE] })
        .then((users) => {
          setEmployeesList(users);
        })
        .catch(console.error);
    }
  }, [isAdmin]);

  // Load projects and manager for current targetUserId (selectedUserId or logged-in user)
  useEffect(() => {
    const targetId = selectedUserId || user?.id;
    if (targetId) {
      setTasksMap({});
      projectService
        .fetchUserProjects(targetId)
        .then((projs) => {
          setUserProjects(projs);
          projs.forEach((p) => {
            projectService
              .fetchTasks(p.id)
              .then((tasks) => {
                setTasksMap((prev) => ({ ...prev, [p.id]: tasks }));
              })
              .catch(console.error);
          });
        })
        .catch(console.error);

      userService
        .getManagerByUserId(targetId)
        .then((m) => {
          if (!m) {
            setManager(null);
          } else {
            setManager({ userid: m.userid, name: m.name });
          }
        })
        .catch(console.error);
    }
  }, [selectedUserId, user]);

  const handleRowChange = (index, field, value) => {
    const updated = [...rows];
    updated[index][field] = value;
    if (field === 'project_id' && value) {
      updated[index].task_id = null;
      if (!tasksMap[value]) {
        projectService
          .fetchTasks(value)
          .then((tasks) => {
            setTasksMap((prev) => ({ ...prev, [value]: tasks }));
          })
          .catch(console.error);
      }
    }
    setRows(updated);
  };

  const handleAddRow = () => {
    setRows([...rows, createEmptyRow()]);
  };

  const handleDeleteRow = (index) => {
    setRows(rows.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    setError('');
    setSuccess('');

    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      if (!r.project_id || !r.task_id || !r.start_time || !r.end_time) {
        setError(`Row #${i + 1} has incomplete required fields`);
        return;
      }
    }

    const targetId = selectedUserId || user?.id;
    if (!targetId) {
      setError('Target user is required');
      return;
    }

    setLoading(true);
    try {
      const payload = rows.map((r) => ({
        project_id: Number(r.project_id),
        task_id: Number(r.task_id),
        start_time: new Date(r.start_time).toISOString(),
        end_time: new Date(r.end_time).toISOString(),
        type: r.type,
        comments: r.comments || null,
      }));

      await timelogService.createTimeLogs(targetId, payload);
      setSuccess('Timesheets submitted successfully!');
      setRows([createEmptyRow()]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit timesheets');
    } finally {
      setLoading(false);
    }
  };

  const employeeOptions = employeesList.map((emp) => ({
    value: String(emp.id),
    label: `${emp.name} (${emp.userid})`,
  }));

  return (
    <Container size="xl" py="xl">
      <Paper p="xl" withBorder radius="md">
        <Group justify="space-between" align="center" mb="lg">
          <Group gap="md" align="center">
            <Title order={2}>Enter Timesheet</Title>
            {isAdmin && (
              <Select
                placeholder="Select Employee"
                data={employeeOptions}
                value={selectedUserId ? String(selectedUserId) : null}
                onChange={(val) => {
                  const newId = val ? Number(val) : user?.id;
                  setSelectedUserId(newId);
                  setRows([createEmptyRow()]);
                }}
                searchable
                style={{ minWidth: 260 }}
              />
            )}
          </Group>
          <Text c="dimmed" size="xl">
            Manager: <strong>({manager ? manager.userid : 'None'}) {manager?.name}</strong>
          </Text>
          <Button
            variant="light"
            leftSection={<IconPlus size={16} />}
            onClick={handleAddRow}
          >
            Add Row
          </Button>
        </Group>

        {error && (
          <Alert color="red" mb="md">
            {error}
          </Alert>
        )}
        {success && (
          <Alert color="green" mb="md">
            {success}
          </Alert>
        )}

        <Stack gap="xs">
          {rows.map((row, index) => (
            <TimesheetRow
              key={index}
              row={row}
              index={index}
              projectsList={userProjects}
              tasksMap={tasksMap}
              onChange={handleRowChange}
              onDelete={handleDeleteRow}
              canDelete={rows.length > 1}
            />
          ))}
        </Stack>

        <Group justify="flex-end" mt="xl">
          <Button variant="default" onClick={() => navigate('/profile')}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={loading}>
            Submit Timesheets
          </Button>
        </Group>
      </Paper>
    </Container>
  );
};

export default EnterTimesheetPage;
