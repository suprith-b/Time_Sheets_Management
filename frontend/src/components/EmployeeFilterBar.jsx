import React from 'react';
import { TextInput, Select, Paper, Group, Text } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { ROLE_OPTIONS } from '../utils/constants';
import CountMultiSelect from './CountMultiSelect';

const STATUS_FILTER_OPTIONS = [
  { value: '1', label: 'Active' },
  { value: '0', label: 'Inactive' },
];

const HAS_MANAGER_OPTIONS = [
  { value: '1', label: 'Yes' },
  { value: '0', label: 'No' },
];

const EmployeeFilterBar = ({
  search,
  setSearch,
  roles,
  setRoles,
  managerId,
  setManagerId,
  managersList,
  status,
  setStatus,
  projects,
  setProjects,
  projectsList,
  hasManager,
  setHasManager,
}) => {
  const managerOptions = managersList.map((m) => ({
    value: String(m.id),
    label: `${m.name} (${m.userid || m.id})`,
  }));

  const projectOptions = projectsList.map((p) => ({
    value: String(p.id),
    label: p.name,
  }));

  return (
    <Paper p="sm" px="md" withBorder mb="lg" radius="md">
      <Group align="flex-end" gap="sm">
        <TextInput
          label={
            <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Search
            </Text>
          }
          placeholder="Employee name..."
          leftSection={<IconSearch size={15} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          size="sm"
          style={{ width: 190 }}
          styles={{ input: { height: 36 } }}
        />
        <CountMultiSelect
          label="Roles"
          placeholder="Roles"
          data={ROLE_OPTIONS}
          value={roles}
          onChange={setRoles}
          style={{ width: 135 }}
        />
        <Select
          label={
            <Text size="xs" fw={600} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Manager
            </Text>
          }
          placeholder="Select Manager"
          data={managerOptions}
          value={managerId ? String(managerId) : null}
          onChange={(val) => setManagerId(val ? Number(val) : null)}
          searchable
          clearable
          size="sm"
          style={{ width: 160 }}
          styles={{ input: { height: 36 } }}
        />
        <CountMultiSelect
          label="Status"
          placeholder="Active / Inactive"
          data={STATUS_FILTER_OPTIONS}
          value={status}
          onChange={setStatus}
          style={{ width: 130 }}
        />
        <CountMultiSelect
          label="Projects"
          placeholder="Projects"
          data={projectOptions}
          value={projects}
          onChange={setProjects}
          searchable
          style={{ width: 140 }}
        />
        <CountMultiSelect
          label="Has Manager"
          placeholder="Yes / No"
          data={HAS_MANAGER_OPTIONS}
          value={hasManager}
          onChange={setHasManager}
          style={{ width: 125 }}
        />
      </Group>
    </Paper>
  );
};

export default EmployeeFilterBar;
