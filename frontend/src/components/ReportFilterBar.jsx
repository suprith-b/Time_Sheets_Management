import React from 'react';
import { Group, Select, Paper, ActionIcon, Box, Text, Tooltip } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { IconArrowDown, IconArrowUp } from '@tabler/icons-react';
import {
  TIMELOG_TYPE_OPTIONS,
  RoleEnum,
} from '../utils/constants';
import CountMultiSelect from './CountMultiSelect';
import { useAuth } from './AuthContext';

const REPORT_SORT_BY_OPTIONS = [
  { value: 'duration', label: 'Duration' },
  { value: 'start_time', label: 'Start Time' },
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
    <Paper p="md" withBorder mb="md">
      <Group grow align="flex-end">
        <CountMultiSelect
          label="View As"
          placeholder="View As"
          data={viewAsOptions}
          value={viewAs}
          onChange={setViewAs}
        />
        <CountMultiSelect
          label="Projects"
          placeholder="Filter projects"
          data={projectOptions}
          value={projects}
          onChange={setProjects}
          searchable
        />
        <CountMultiSelect
          label="Type"
          placeholder="Standard / Overtime"
          data={TIMELOG_TYPE_OPTIONS}
          value={type}
          onChange={setType}
        />
      </Group>

      <Group grow align="flex-end" mt="md">
        <DateInput
          label="Start Date"
          placeholder="Select start date"
          value={startDate}
          onChange={setStartDate}
          clearable
        />
        <DateInput
          label="End Date"
          placeholder="Select end date"
          value={endDate}
          onChange={setEndDate}
          clearable
        />
        <Group gap="xs" align="flex-end" style={{ flex: 1 }}>
          <Select
            label="Sort By"
            data={REPORT_SORT_BY_OPTIONS}
            value={sortBy}
            onChange={setSortBy}
            style={{ flex: 1 }}
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
      </Group>
    </Paper>
  );
};

export default ReportFilterBar;
