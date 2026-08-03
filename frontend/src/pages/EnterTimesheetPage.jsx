import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Title,
  Button,
  Group,
  Stack,
  Alert,
} from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import TimesheetRow from '../components/TimesheetRow';
import { projectService } from '../services/projectService';
import { timelogService } from '../services/timelogService';
import { TypeEnum } from '../utils/constants';

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
  const { user } = useAuth();

  const [rows, setRows] = useState([createEmptyRow()]);
  const [userProjects, setUserProjects] = useState([]);
  const [tasksMap, setTasksMap] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (user) {
      projectService
        .fetchUserProjects(user.id)
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
    }
  }, [user]);

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

    setLoading(true);
    try {
      const payload = rows.map((r) => ({
        project_id: Number(r.project_id),
        task_id: Number(r.task_id),
        start_time: new Date( r.start_time).toISOString(), 
        end_time: new Date( r.end_time).toISOString(),
        type: r.type,
        comments: r.comments || null,
      }));

      await timelogService.createTimeLogs(user.id, payload);
      setSuccess('Timesheets submitted successfully!');
      setRows([createEmptyRow()]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit timesheets');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="xl" py="xl">
      <Paper p="xl" withBorder radius="md">
        <Group justify="space-between" mb="lg">
          <Title order={2}>Enter Timesheet</Title>
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
