import React from 'react';
import { Table, Select, Text, Badge, Button } from '@mantine/core';
import { IconUsers } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { RoleEnum, STATUS_OPTIONS, STATUS_OPTIONS_FOR_MANAGER } from '../utils/constants';
import { formatDate } from '../utils/formatters';

const getStatusBadgeColor = (status) => {
  switch (status) {
    case 'in_progress':
      return 'indigo';
    case 'completed':
      return 'teal';
    case 'on_hold':
      return 'amber';
    case 'archived':
      return 'gray';
    default:
      return 'gray';
  }
};

const ProjectTable = ({ projects, onStatusChange }) => {
  const navigate = useNavigate();
  const { isOneOfRoles } = useAuth();
  const canEditStatus = isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]);
  const isAdmin = isOneOfRoles([RoleEnum.ADMIN]);

  const rows = projects.map((p) => (
    <Table.Tr
      key={p.id}
      style={{ cursor: 'pointer' }}
      onClick={() => navigate(`/projects/${p.id}`)}
    >
      <Table.Td>
        <Text fw={600} c="dark">{p.name}</Text>
      </Table.Td>
      <Table.Td>{p.num_tasks ?? 0}</Table.Td>
      <Table.Td>{p.duration} days</Table.Td>
      <Table.Td>{formatDate(p.end_date)}</Table.Td>
      <Table.Td>
        {canEditStatus ? (
          <Select
            size="xs"
            data={isAdmin ? STATUS_OPTIONS : STATUS_OPTIONS_FOR_MANAGER}
            value={p.status}
            onChange={(val) => val && onStatusChange(p.id, val)}
            onClick={(e) => e.stopPropagation()}
            style={{ width: 140 }}
          />
        ) : (
          <Badge variant="light" color={getStatusBadgeColor(p.status)}>
            {p.status}
          </Badge>
        )}
      </Table.Td>
      {canEditStatus && (
        <Table.Td>
          <Button
            size="xs"
            variant="light"
            color="indigo"
            leftSection={<IconUsers size={14} />}
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/projects/${p.id}/employees`);
            }}
          >
            Manage Employees
          </Button>
        </Table.Td>
      )}
    </Table.Tr>
  ));

  return (
    <Table highlightOnHover withTableBorder>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Project Name</Table.Th>
          <Table.Th>Tasks</Table.Th>
          <Table.Th>Duration</Table.Th>
          <Table.Th>End Date</Table.Th>
          <Table.Th>Status</Table.Th>
          {canEditStatus && <Table.Th>Actions</Table.Th>}
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.length > 0 ? (
          rows
        ) : (
          <Table.Tr>
            <Table.Td colSpan={canEditStatus ? 6 : 5} align="center">
              No projects found
            </Table.Td>
          </Table.Tr>
        )}
      </Table.Tbody>
    </Table>
  );
};

export default ProjectTable;
