import React from 'react';
import { Group, TextInput, Select, Paper, ActionIcon, Tooltip } from '@mantine/core';
import { IconSearch, IconArrowDown, IconArrowUp } from '@tabler/icons-react';
import { STATUS_OPTIONS } from '../utils/constants';
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
  const isDescending = Number(sortType) === -1;

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
        <Group gap="xs" align="flex-end" style={{ flex: 1 }}>
          <Select
            label="Sort By"
            data={SORT_BY_OPTIONS}
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

export default ProjectFilterBar;
