import React from 'react';
import { Table, Select, Text, Badge } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { RoleEnum, STATUS_OPTIONS } from '../utils/constants';
import { formatDate } from '../utils/formatters';

const ProjectTable = ({ projects, onStatusChange }) => {
  const navigate = useNavigate();
  const { isOneOfRoles } = useAuth();
  const canEditStatus = isOneOfRoles([RoleEnum.ADMIN, RoleEnum.MANAGER]);

  const rows = projects.map((p) => (
    <Table.Tr
      key={p.id}
      style={{ cursor: 'pointer' }}
      onClick={() => navigate(`/projects/${p.id}`)}
    >
      <Table.Td>
        <Text fw={500}>{p.name}</Text>
      </Table.Td>
      <Table.Td>{p.num_tasks ?? 0}</Table.Td>
      <Table.Td>{p.duration} days</Table.Td>
      <Table.Td>{formatDate(p.end_date)}</Table.Td>
      <Table.Td onClick={(e) => e.stopPropagation()}>
        {canEditStatus ? (
          <Select
            size="xs"
            data={STATUS_OPTIONS}
            value={p.status}
            onChange={(val) => val && onStatusChange(p.id, val)}
            style={{ width: 140 }}
          />
        ) : (
          <Badge variant="light">{p.status}</Badge>
        )}
      </Table.Td>
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
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.length > 0 ? (
          rows
        ) : (
          <Table.Tr>
            <Table.Td colSpan={5} align="center">
              No projects found
            </Table.Td>
          </Table.Tr>
        )}
      </Table.Tbody>
    </Table>
  );
};

export default ProjectTable;
