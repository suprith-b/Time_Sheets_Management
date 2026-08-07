import React, { useState, useEffect } from 'react';
import { Paper, Group, Select, Table, Badge, Text, ActionIcon, Tooltip, Title, Container } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { IconArrowDown, IconArrowUp } from '@tabler/icons-react';
import { timelogService } from '../services/timelogService';
import { projectService } from '../services/projectService';
import { TIMELOG_TYPE_OPTIONS } from '../utils/constants';
import { formatDateTime } from '../utils/formatters';
import CountMultiSelect from './CountMultiSelect';
import { useParams } from 'react-router-dom';
import { userService } from '../services/userService';

const LOG_SORT_BY_OPTIONS = [
  { value: 'start_time', label: 'Start Time' },
  { value: 'duration', label: 'Duration' },
];

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
  const [ user, setUser ] = useState( null );

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
    setLoading( true );
    try{
      const user = await userService.getUserById(userId);
      setUser(user);
    }catch(err){
      console.error('Failed to load user:', err);
    }finally{
      setLoading(false);
    }
  }


  useEffect(() => {
    loadLogs();
  }, [userId, selectedProjects, selectedTypes, startDate, endDate, sortBy, sortType]);

  const projectSelectOptions = userProjects.map((p) => ({
    value: String(p.id),
    label: p.name,
  }));

  return (
    <Container size="lg" py="xl">
      {user &&
         <Title order={2} mb="lg">
          TimeLogs: {user.name}
        </Title>}
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

      <Table highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Project Name</Table.Th>
            <Table.Th>Task Name</Table.Th>
            <Table.Th>Start Time</Table.Th>
            <Table.Th>End Time</Table.Th>
            <Table.Th>Type</Table.Th>
            <Table.Th>Comments</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {logs.length > 0 ? (
            logs.map((log) => (
              <Table.Tr key={log.id}>
                <Table.Td>
                  <Text fw={500}>{log.project_name}</Text>
                </Table.Td>
                <Table.Td>{log.task_name}</Table.Td>
                <Table.Td>{formatDateTime(log.start_time)}</Table.Td>
                <Table.Td>{formatDateTime(log.end_time)}</Table.Td>
                <Table.Td>
                  <Badge color={log.type === 'standard' ? 'blue' : 'orange'}>
                    {log.type}
                  </Badge>
                </Table.Td>
                <Table.Td>{log.comments || '—'}</Table.Td>
              </Table.Tr>
            ))
          ) : (
            <Table.Tr>
              <Table.Td colSpan={6} align="center">
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
