import React, { useState, useEffect } from 'react';
import { Paper, Group, Select, Table, Badge, Text, ActionIcon, Tooltip, Title, Container, TextInput, Alert } from '@mantine/core';
import { DateInput, DateTimePicker } from '@mantine/dates';
import { IconArrowDown, IconArrowUp, IconEdit, IconCheck, IconX } from '@tabler/icons-react';
import { timelogService } from '../services/timelogService';
import { projectService } from '../services/projectService';
import { TIMELOG_TYPE_OPTIONS, RoleEnum } from '../utils/constants';
import { formatDateTime } from '../utils/formatters';
import CountMultiSelect from './CountMultiSelect';
import { useParams } from 'react-router-dom';
import { userService } from '../services/userService';
import { useAuth } from './AuthContext';

const LOG_SORT_BY_OPTIONS = [
  { value: 'start_time', label: 'Start Time' },
  { value: 'duration', label: 'Duration' },
];

const calculateHours = (start, end) => {
  if (!start || !end) return '0.00';
  const startTime = new Date(start);
  const endTime = new Date(end);
  const diffMs = endTime - startTime;
  if (isNaN(diffMs) || diffMs < 0) return '0.00';
  return (diffMs / (1000 * 60 * 60)).toFixed(2);
};

const LogsSection = ({ userId }) => {
  const [logs, setLogs] = useState([]);
  const [userProjects, setUserProjects] = useState([]);
  const [selectedProjects, setSelectedProjects] = useState([]);
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [sortBy, setSortBy] = useState('start_time');
  const [sortType, setSortType] = useState(-1);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);

  // Inline editing states
  const [editingLogId, setEditingLogId] = useState(null);
  const [editForm, setEditForm] = useState({
    start_time: null,
    end_time: null,
    type: 'standard',
    comments: '',
  });
  const [editError, setEditError] = useState('');
  const [savingLogId, setSavingLogId] = useState(null);

  const { isOneOfRoles } = useAuth();
  const isAdmin = isOneOfRoles([RoleEnum.ADMIN]);

  const isDescending = Number(sortType) === -1;

  const { userIdParam } = useParams();

  useEffect(() => {
    if (userIdParam) {
      userId = userIdParam;
      loadUser();
    }
  }, [userIdParam]);

  useEffect(() => {
    projectService.fetchUserProjects(userId).then(setUserProjects).catch(console.error);
  }, [userId]);

  const loadLogs = async () => {
    setLoading(true);
    try {
      const data = await timelogService.getUserTimeLogs(userId, {
        projectIds: selectedProjects.map(Number),
        type: selectedTypes,
        startDate: startDate ? startDate.toISOString() : null,
        endDate: endDate ? endDate.toISOString() : null,
        sortBy,
        sortType,
      });
      setLogs(data);
    } catch (err) {
      console.error('Failed to load user timelogs:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadUser = async () => {
    setLoading(true);
    try {
      const u = await userService.getUserById(userId);
      setUser(u);
    } catch (err) {
      console.error('Failed to load user:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [userId, selectedProjects, selectedTypes, startDate, endDate, sortBy, sortType]);

  const handleStartEdit = (log) => {
    setEditingLogId(log.id);
    setEditForm({
      start_time: log.start_time ? new Date(log.start_time) : null,
      end_time: log.end_time ? new Date(log.end_time) : null,
      type: log.type,
      comments: log.comments || '',
    });
    setEditError('');
  };

  const handleCancelEdit = () => {
    setEditingLogId(null);
    setEditError('');
  };

  const handleSaveEdit = async (logId) => {
    setEditError('');

    if (!editForm.start_time || !editForm.end_time) {
      setEditError('Start time and End time are required.');
      return;
    }

    if (new Date(editForm.start_time) > new Date(editForm.end_time)) {
      setEditError('Start time cannot be after End time.');
      return;
    }

    setSavingLogId(logId);
    try {
      await timelogService.updateTimeLog(logId, {
        start_time: new Date(editForm.start_time).toISOString(),
        end_time: new Date(editForm.end_time).toISOString(),
        type: editForm.type,
        comments: editForm.comments || null,
      });
      setEditingLogId(null);
      await loadLogs();
    } catch (err) {
      setEditError(err.response?.data?.detail || 'Failed to update time log');
    } finally {
      setSavingLogId(null);
    }
  };

  const projectSelectOptions = userProjects.map((p) => ({
    value: String(p.id),
    label: p.name,
  }));

  const totalColumns = isAdmin ? 8 : 7;

  return (
    <Container size="lg" py="xl">
      {user && (
        <Title order={2} mb="lg">
          TimeLogs: {user.name}
        </Title>
      )}
      <Paper p="md" withBorder mb="md">
        <Group grow align="flex-end">
          <CountMultiSelect
            label="Projects"
            placeholder="Filter projects"
            data={projectSelectOptions}
            value={selectedProjects}
            onChange={setSelectedProjects}
            searchable
          />
          <CountMultiSelect
            label="Type"
            placeholder="Standard / Overtime"
            data={TIMELOG_TYPE_OPTIONS}
            value={selectedTypes}
            onChange={setSelectedTypes}
          />
          <DateInput
            label="Start Date"
            placeholder="Start date"
            value={startDate}
            onChange={setStartDate}
            clearable
          />
          <DateInput
            label="End Date"
            placeholder="End date"
            value={endDate}
            onChange={setEndDate}
            clearable
          />
        </Group>

        <Group gap="xs" align="flex-end" mt="md">
          <Select
            label="Sort By"
            data={LOG_SORT_BY_OPTIONS}
            value={sortBy}
            onChange={setSortBy}
            style={{ width: 220 }}
          />
          <Tooltip label={isDescending ? 'Descending' : 'Ascending'}>
            <ActionIcon
              variant="light"
              color={isDescending ? 'red' : 'blue'}
              size={36}
              radius="sm"
              onClick={() => setSortType(isDescending ? 1 : -1)}
              aria-label="Toggle Sort Order"
            >
              {isDescending ? (
                <IconArrowDown size={20} />
              ) : (
                <IconArrowUp size={20} />
              )}
            </ActionIcon>
          </Tooltip>
        </Group>
      </Paper>

      {editError && (
        <Alert color="red" mb="md" withCloseButton onClose={() => setEditError('')}>
          {editError}
        </Alert>
      )}

      <Table highlightOnHover withTableBorder style={{ verticalAlign: 'middle' }}>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Project Name</Table.Th>
            <Table.Th>Task Name</Table.Th>
            <Table.Th>Start Time</Table.Th>
            <Table.Th>End Time</Table.Th>
            <Table.Th>Hours</Table.Th>
            <Table.Th>Type</Table.Th>
            <Table.Th>Comments</Table.Th>
            {isAdmin && <Table.Th style={{ width: 90 }}>Actions</Table.Th>}
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {logs.length > 0 ? (
            logs.map((log) => {
              const isEditing = log.id === editingLogId;
              const durationHours = isEditing
                ? calculateHours(editForm.start_time, editForm.end_time)
                : calculateHours(log.start_time, log.end_time);

              if (isEditing) {
                return (
                  <Table.Tr key={log.id}>
                    <Table.Td>
                      <Text fw={500}>{log.project_name}</Text>
                    </Table.Td>
                    <Table.Td>{log.task_name}</Table.Td>
                    <Table.Td>
                      <DateTimePicker
                        value={editForm.start_time}
                        onChange={(val) => setEditForm((prev) => ({ ...prev, start_time: val }))}
                        size="xs"
                        style={{ minWidth: 170 }}
                      />
                    </Table.Td>
                    <Table.Td>
                      <DateTimePicker
                        value={editForm.end_time}
                        onChange={(val) => setEditForm((prev) => ({ ...prev, end_time: val }))}
                        size="xs"
                        style={{ minWidth: 170 }}
                      />
                    </Table.Td>
                    <Table.Td>
                      <Text size="sm" fw={600}>
                        {durationHours} hrs
                      </Text>
                    </Table.Td>
                    <Table.Td>
                      <Select
                        data={TIMELOG_TYPE_OPTIONS}
                        value={editForm.type}
                        onChange={(val) => setEditForm((prev) => ({ ...prev, type: val }))}
                        size="xs"
                        style={{ width: 110 }}
                      />
                    </Table.Td>
                    <Table.Td>
                      <TextInput
                        value={editForm.comments}
                        onChange={(e) => setEditForm((prev) => ({ ...prev, comments: e.target.value }))}
                        size="xs"
                        placeholder="Comments"
                      />
                    </Table.Td>
                    <Table.Td>
                      <Group gap={4} wrap="nowrap">
                        <ActionIcon
                          color="green"
                          variant="light"
                          size="sm"
                          onClick={() => handleSaveEdit(log.id)}
                          loading={savingLogId === log.id}
                          title="Save"
                        >
                          <IconCheck size={16} />
                        </ActionIcon>
                        <ActionIcon
                          color="gray"
                          variant="light"
                          size="sm"
                          onClick={handleCancelEdit}
                          title="Cancel"
                        >
                          <IconX size={16} />
                        </ActionIcon>
                      </Group>
                    </Table.Td>
                  </Table.Tr>
                );
              }

              return (
                <Table.Tr key={log.id}>
                  <Table.Td>
                    <Text fw={500}>{log.project_name}</Text>
                  </Table.Td>
                  <Table.Td>{log.task_name}</Table.Td>
                  <Table.Td>{formatDateTime(log.start_time)}</Table.Td>
                  <Table.Td>{formatDateTime(log.end_time)}</Table.Td>
                  <Table.Td>
                    <Text size="sm" fw={500}>
                      {durationHours} hrs
                    </Text>
                  </Table.Td>
                  <Table.Td>
                    <Badge color={log.type === 'standard' ? 'blue' : 'orange'}>
                      {log.type}
                    </Badge>
                  </Table.Td>
                  <Table.Td>{log.comments || '—'}</Table.Td>
                  {isAdmin && (
                    <Table.Td>
                      <ActionIcon
                        color="blue"
                        variant="subtle"
                        size="sm"
                        onClick={() => handleStartEdit(log)}
                        title="Edit Log"
                      >
                        <IconEdit size={16} />
                      </ActionIcon>
                    </Table.Td>
                  )}
                </Table.Tr>
              );
            })
          ) : (
            <Table.Tr>
              <Table.Td colSpan={totalColumns} align="center">
                {loading ? 'Loading logs...' : 'No time logs found'}
              </Table.Td>
            </Table.Tr>
          )}
        </Table.Tbody>
      </Table>
    </Container>
  );
};

export default LogsSection;
