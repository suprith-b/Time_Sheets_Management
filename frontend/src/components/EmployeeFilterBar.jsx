import React from 'react';
import { Group, TextInput, Select, Paper } from '@mantine/core';
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
    <Paper p="md" withBorder mb="md">
      <Group grow align="flex-end">
        <TextInput
          label="Search Employee"
          placeholder="Search by name..."
          leftSection={<IconSearch size={16} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <CountMultiSelect
          label="Roles"
          placeholder="Filter roles"
          data={ROLE_OPTIONS}
          value={roles}
          onChange={setRoles}
        />
        <Select
          label="Manager"
          placeholder="Select Manager"
          data={managerOptions}
          value={managerId ? String(managerId) : null}
          onChange={(val) => setManagerId(val ? Number(val) : null)}
          searchable
          clearable
        />
        <CountMultiSelect
          label="Status"
          placeholder="Active / Inactive"
          data={STATUS_FILTER_OPTIONS}
          value={status}
          onChange={setStatus}
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
          label="Has Manager"
          placeholder="Yes / No"
          data={HAS_MANAGER_OPTIONS}
          value={hasManager}
          onChange={setHasManager}
        />
      </Group>
    </Paper>
  );
};

export default EmployeeFilterBar;
