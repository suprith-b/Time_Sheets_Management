import React from 'react';
import { Group, Select, Paper, ActionIcon, Tooltip, Text } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { IconArrowDown, IconArrowUp, IconCalendar } from '@tabler/icons-react';
import {
  TIMELOG_TYPE_OPTIONS,
  RoleEnum,
} from '../utils/constants';
import CountMultiSelect from './CountMultiSelect';
import { useAuth } from './AuthContext';

const REPORT_SORT_BY_OPTIONS = [
  { value: 'duration', label: 'Duration' },
  { value: 'project_name', label: 'Project Name' },
];

const ReportFilterBar = ({
  viewAs,
  setViewAs,
  projects,
  setProjects,
  projectsList,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  type,
  setType,
  sortBy,
  setSortBy,
  sortType,
  setSortType,
}) => {
  const { user: currentUser, hasRole } = useAuth();
  const rawRoles = currentUser?.roles || [];
  const normalizedRoles = rawRoles.map((r) => String(r).toLowerCase());

  const hasAdmin =
    (hasRole && hasRole(RoleEnum.ADMIN)) ||
    normalizedRoles.includes('admin');
  const hasManager =
    (hasRole && hasRole(RoleEnum.MANAGER)) ||
    normalizedRoles.includes('manager');

  const viewAsOptions = [];
  if (hasAdmin) {
    viewAsOptions.push({ value: RoleEnum.ADMIN, label: 'ADMIN' });
  }
  if (hasManager) {
    viewAsOptions.push({ value: RoleEnum.MANAGER, label: 'MANAGER' });
  }
  const projectOptions = projectsList.map((p) => ({
    value: String(p.id),
    label: p.name,
  }));

  const isDescending = Number(sortType) === -1;

  return (
    <Paper p="sm" px="md" withBorder mb="lg" radius="md">
      <Group align="flex-end" gap="sm">
        <CountMultiSelect
          label="View As"
          placeholder="View As"
          data={viewAsOptions}
          value={viewAs}
          onChange={setViewAs}
          style={{ width: 135 }}
        />
        <CountMultiSelect
          label="Projects"
          placeholder="Projects"
          data={projectOptions}
          value={projects}
          onChange={setProjects}
          searchable
          style={{ width: 150 }}
        />
        <CountMultiSelect
          label="Type"
          placeholder="Type"
          data={TIMELOG_TYPE_OPTIONS}
          value={type}
          onChange={setType}
          style={{ width: 145 }}
        />
        <DateInput
          label={
            <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Start Date
            </Text>
          }
          placeholder="Start date"
          leftSection={<IconCalendar size={15} />}
          value={startDate}
          onChange={setStartDate}
          clearable
          size="sm"
          style={{ width: 135 }}
          styles={{ input: { height: 36 } }}
        />
        <DateInput
          label={
            <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              End Date
            </Text>
          }
          placeholder="End date"
          leftSection={<IconCalendar size={15} />}
          value={endDate}
          onChange={setEndDate}
          clearable
          size="sm"
          style={{ width: 135 }}
          styles={{ input: { height: 36 } }}
        />
        <Group gap={6} align="flex-end">
          <Select
            label={
              <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                Sort By
              </Text>
            }
            data={REPORT_SORT_BY_OPTIONS}
            value={sortBy}
            onChange={setSortBy}
            size="sm"
            style={{ width: 130 }}
            styles={{ input: { height: 36 } }}
          />
          <Tooltip label={isDescending ? 'Descending' : 'Ascending'}>
            <ActionIcon
              variant="light"
              color={isDescending ? 'indigo' : 'gray'}
              size={36}
              radius="md"
              onClick={() => setSortType(isDescending ? 1 : -1)}
              aria-label="Toggle Sort Order"
            >
              {isDescending ? (
                <IconArrowDown size={16} />
              ) : (
                <IconArrowUp size={16} />
              )}
            </ActionIcon>
          </Tooltip>
        </Group>
      </Group>
    </Paper>
  );
};

export default ReportFilterBar;
