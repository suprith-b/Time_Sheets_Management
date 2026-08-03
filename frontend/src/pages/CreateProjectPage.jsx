import React, { useState } from 'react';
import {
  Container,
  Paper,
  Title,
  TextInput,
  Textarea,
  NumberInput,
  Select,
  Button,
  Group,
  Stack,
  Alert,
  ActionIcon,
  Text,
} from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { IconPlus, IconTrash } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { StatusEnum, STATUS_OPTIONS } from '../utils/constants';

const CreateProjectPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    duration: 30,
    status: StatusEnum.CREATED,
    start_date: null,
    end_date: null,
  });

  const [tasks, setTasks] = useState([{ name: '', description: '' }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTaskChange = (index, field, value) => {
    const updated = [...tasks];
    updated[index][field] = value;
    setTasks(updated);
  };

  const addTaskRow = () => {
    setTasks([...tasks, { name: '', description: '' }]);
  };

  const removeTaskRow = (index) => {
    setTasks(tasks.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const validTasks = tasks.filter((t) => t.name.trim() !== '');
      await projectService.createProject({
        name: formData.name,
        duration: Number(formData.duration),
        status: formData.status,
        start_date: formData.start_date
          ? formData.start_date.toISOString().split('T')[0]
          : null,
        end_date: formData.end_date
          ? formData.end_date.toISOString().split('T')[0]
          : null,
        tasks: validTasks,
      });
      navigate('/projects');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="sm" py="xl">
      <Paper p="xl" withBorder radius="md">
        <Title order={3} mb="lg">
          Create New Project
        </Title>

        {error && (
          <Alert color="red" mb="md">
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <Stack gap="md">
            <TextInput
              label="Project Name"
              placeholder="e.g. Website Redesign"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />

            <Select
              label="Status"
              data={STATUS_OPTIONS}
              value={formData.status}
              onChange={(val) => setFormData({ ...formData, status: val })}
            />

            <NumberInput
              label="Duration (in days)"
              required
              value={formData.duration}
              onChange={(val) => setFormData({ ...formData, duration: Number(val) })}
            />

            <Group grow>
              <DateInput
                label="Start Date"
                placeholder="Start Date"
                value={formData.start_date}
                onChange={(val) => setFormData({ ...formData, start_date: val })}
              />
              <DateInput
                label="End Date"
                placeholder="End Date"
                value={formData.end_date}
                onChange={(val) => setFormData({ ...formData, end_date: val })}
              />
            </Group>

            <div>
              <Group justify="space-between" mb="xs">
                <Text fw={500} size="sm">
                  Initial Tasks (Optional)
                </Text>
                <Button
                  size="xs"
                  variant="light"
                  leftSection={<IconPlus size={14} />}
                  onClick={addTaskRow}
                >
                  Add Task Row
                </Button>
              </Group>

              {tasks.map((t, idx) => (
                <Paper key={idx} p="xs" withBorder mb="xs" bg="gray.0">
                  <Group wrap="nowrap" align="flex-start">
                    <Stack gap="xs" style={{ flex: 1 }}>
                      <TextInput
                        placeholder="Task Name"
                        value={t.name}
                        onChange={(e) =>
                          handleTaskChange(idx, 'name', e.target.value)
                        }
                      />
                      <Textarea
                        placeholder="Task Description"
                        value={t.description}
                        onChange={(e) =>
                          handleTaskChange(idx, 'description', e.target.value)
                        }
                      />
                    </Stack>
                    <ActionIcon
                      color="red"
                      variant="subtle"
                      onClick={() => removeTaskRow(idx)}
                      disabled={tasks.length === 1}
                      mt={4}
                    >
                      <IconTrash size={16} />
                    </ActionIcon>
                  </Group>
                </Paper>
              ))}
            </div>

            <Group justify="flex-end" mt="md">
              <Button variant="default" onClick={() => navigate('/projects')}>
                Cancel
              </Button>
              <Button type="submit" loading={loading}>
                Create Project
              </Button>
            </Group>
          </Stack>
        </form>
      </Paper>
    </Container>
  );
};

export default CreateProjectPage;
