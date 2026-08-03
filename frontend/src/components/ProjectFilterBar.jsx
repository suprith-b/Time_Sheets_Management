import React from 'react';
import { Group, TextInput, Select, Paper } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { STATUS_OPTIONS, SORT_ORDER_OPTIONS } from '../utils/constants';
import CountMultiSelect from './CountMultiSelect';

const SORT_BY_OPTIONS = [
  { value: 'duration', label: 'Duration' },
  { value: 'end_time', label: 'End Date' },
];

const ProjectFilterBar = ({
  search,
  setSearch,
  status,
  setStatus,
  sortBy,
  setSortBy,
  sortType,
  setSortType,
}) => {
  return (
    <Paper p="md" withBorder mb="md">
      <Group grow align="flex-end">
        <TextInput
          label="Search Project"
          placeholder="Search by name..."
          leftSection={<IconSearch size={16} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <CountMultiSelect
          label="Status"
          placeholder="Filter status"
          data={STATUS_OPTIONS}
          value={status}
          onChange={setStatus}
        />
        <Select
          label="Sort By"
          data={SORT_BY_OPTIONS}
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

export default ProjectFilterBar;
