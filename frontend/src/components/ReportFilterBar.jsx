import React from 'react';
import { Group, Select, Paper } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import {
  TIMELOG_TYPE_OPTIONS,
  SORT_ORDER_OPTIONS,
} from '../utils/constants';
import CountMultiSelect from './CountMultiSelect';

const REPORT_SORT_BY_OPTIONS = [
  { value: 'duration', label: 'Duration' },
  { value: 'start_time', label: 'Start Time' },
  { value: 'project_name', label: 'Project Name' },
];

const ReportFilterBar = ({
  roles,
  setRoles,
  managers,
  setManagers,
  managersList,
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
  const managerOptions = managersList.map((m) => ({
    value: String(m.id),
    label: m.name,
  }));

  const projectOptions = projectsList.map((p) => ({
    value: String(p.id),
    label: p.name,
  }));

  return (
    <Paper p="md" withBorder mb="md">
      <Group grow align="flex-end">
        <CountMultiSelect
          label="Managers"
          placeholder="Filter managers"
          data={managerOptions}
          value={managers}
          onChange={setManagers}
          searchable
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
        <Select
          label="Sort By"
          data={REPORT_SORT_BY_OPTIONS}
          value={sortBy}
          onChange={setSortBy}
        />
        <Select
          label="Sort Order"
          data={SORT_ORDER_OPTIONS}
          value={String(sortType)}
          onChange={(val) => setSortType(Number(val))}
        />
      </Group>
    </Paper>
  );
};

export default ReportFilterBar;
