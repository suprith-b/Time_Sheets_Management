import React from 'react';
import { Group, TextInput, Select, Paper, ActionIcon, Tooltip, Text } from '@mantine/core';
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
    <Paper p="sm" px="md" withBorder mb="lg" radius="md">
      <Group align="flex-end" gap="md" wrap="nowrap">
        <TextInput
          label={
            <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Search
            </Text>
          }
          placeholder="Project name..."
          leftSection={<IconSearch size={15} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          size="sm"
          style={{ width: 220 }}
          styles={{ input: { height: 36 } }}
        />
        <CountMultiSelect
          label="Status"
          placeholder="Filter status"
          data={STATUS_OPTIONS}
          value={status}
          onChange={setStatus}
          style={{ width: 160 }}
        />
        <Select
          label={
            <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Sort By
            </Text>
          }
          data={SORT_BY_OPTIONS}
          value={sortBy}
          onChange={setSortBy}
          size="sm"
          style={{ width: 140 }}
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
    </Paper>
  );
};

export default ProjectFilterBar;
