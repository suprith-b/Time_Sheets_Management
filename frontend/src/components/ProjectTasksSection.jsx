import React, { useState } from 'react';
import {
  Paper,
  Title,
  TextInput,
  Textarea,
  Button,
  Group,
  Table,
  ActionIcon,
  Text,
} from '@mantine/core';
import { IconSearch, IconPencil, IconTrash, IconPlus } from '@tabler/icons-react';
import { projectService } from '../services/projectService';

const ProjectTasksSection = ({
  projectId,
  tasks = [],
  canManage,
  onTasksUpdated,
}) => {
  const [search, setSearch] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [taskForm, setTaskForm] = useState({ name: '', description: '' });
  const [showAddForm, setShowAddForm] = useState(false);
  const [loading, setLoading] = useState(false);

  const filteredTasks = tasks.filter(
    (t) =>
      t.name.toLowerCase().includes(search.toLowerCase()) ||
      (t.description && t.description.toLowerCase().includes(search.toLowerCase()))
  );

  const handleCreate = async () => {
    if (!taskForm.name) return;
    setLoading(true);
    try {
      await projectService.createTask(projectId, taskForm);
      setTaskForm({ name: '', description: '' });
      setShowAddForm(false);
      onTasksUpdated();
    } catch (err) {
      console.error('Failed to create task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (taskId) => {
    setLoading(true);
    try {
      await projectService.updateTask(taskId, taskForm);
      setEditingTaskId(null);
      setTaskForm({ name: '', description: '' });
      onTasksUpdated();
    } catch (err) {
      console.error('Failed to update task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (taskId) => {
    try {
      await projectService.deleteTask(taskId);
      onTasksUpdated();
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const startEdit = (t) => {
    setEditingTaskId(t.id);
    setTaskForm({ name: t.name, description: t.description || '' });
  };

  return (
    <Paper p="md" withBorder mt="md">
      <Group justify="space-between" mb="md">
        <Title order={4}>Tasks</Title>
        <Group>
          <TextInput
            placeholder="Search tasks..."
            leftSection={<IconSearch size={16} />}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          {canManage && !showAddForm && (
            <Button
              leftSection={<IconPlus size={16} />}
              size="sm"
              onClick={() => {
                setShowAddForm(true);
                setTaskForm({ name: '', description: '' });
              }}
            >
              Add Task
            </Button>
          )}
        </Group>
      </Group>

      {showAddForm && (
        <Paper p="sm" withBorder mb="md" bg="gray.0">
          <Text fw={500} size="sm" mb="xs">
            Create New Task
          </Text>
          <TextInput
            placeholder="Task Name"
            value={taskForm.name}
            onChange={(e) => setTaskForm({ ...taskForm, name: e.target.value })}
            mb="xs"
          />
          <Textarea
            placeholder="Task Description"
            value={taskForm.description}
            onChange={(e) => setTaskForm({ ...taskForm, description: e.target.value })}
            mb="xs"
          />
          <Group justify="flex-end">
            <Button size="xs" onClick={handleCreate} loading={loading}>
              Save Task
            </Button>
            <Button size="xs" variant="default" onClick={() => setShowAddForm(false)}>
              Cancel
            </Button>
          </Group>
        </Paper>
      )}

      <Table highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>Description</Table.Th>
            {canManage && <Table.Th>Actions</Table.Th>}
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {filteredTasks.length > 0 ? (
            filteredTasks.map((t) => (
              <Table.Tr key={t.id}>
                {editingTaskId === t.id ? (
                  <>
                    <Table.Td colSpan={2}>
                      <TextInput
                        value={taskForm.name}
                        onChange={(e) =>
                          setTaskForm({ ...taskForm, name: e.target.value })
                        }
                        mb="xs"
                      />
                      <Textarea
                        value={taskForm.description}
                        onChange={(e) =>
                          setTaskForm({ ...taskForm, description: e.target.value })
                        }
                      />
                    </Table.Td>
                    <Table.Td>
                      <Group gap="xs">
                        <Button
                          size="xs"
                          onClick={() => handleUpdate(t.id)}
                          loading={loading}
                        >
                          Save
                        </Button>
                        <Button
                          size="xs"
                          variant="default"
                          onClick={() => setEditingTaskId(null)}
                        >
                          Cancel
                        </Button>
                      </Group>
                    </Table.Td>
                  </>
                ) : (
                  <>
                    <Table.Td>
                      <Text fw={500}>{t.name}</Text>
                    </Table.Td>
                    <Table.Td>{t.description || '-'}</Table.Td>
                    {canManage && (
                      <Table.Td>
                        <Group gap="xs">
                          <ActionIcon
                            variant="subtle"
                            color="blue"
                            onClick={() => startEdit(t)}
                          >
                            <IconPencil size={16} />
                          </ActionIcon>
                          <ActionIcon
                            variant="subtle"
                            color="red"
                            onClick={() => handleDelete(t.id)}
                          >
                            <IconTrash size={16} />
                          </ActionIcon>
                        </Group>
                      </Table.Td>
                    )}
                  </>
                )}
              </Table.Tr>
            ))
          ) : (
            <Table.Tr>
              <Table.Td colSpan={canManage ? 3 : 2} align="center">
                No tasks found
              </Table.Td>
            </Table.Tr>
          )}
        </Table.Tbody>
      </Table>
    </Paper>
  );
};

export default ProjectTasksSection;
