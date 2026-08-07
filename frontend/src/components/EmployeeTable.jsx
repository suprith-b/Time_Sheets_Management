import { useState, React } from 'react';
import { Table, Badge, Button, Text, Group } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { RoleEnum } from '../utils/constants';

const EmployeeTable = ({ employees, onToggleStatus, setShowTimeLogs }) => {
  const navigate = useNavigate();
  const { isOneOfRoles } = useAuth();
  const isAdmin = isOneOfRoles([RoleEnum.ADMIN]);
  const isManager = isOneOfRoles([ RoleEnum.MANAGER ] );
  const rows = employees.map((emp) => (
    <Table.Tr
      key={emp.id}
      style={{ cursor: 'pointer' }}
      onClick={() => navigate(`/employees/${emp.id}`)}
    >
      <Table.Td>{emp.userid || emp.id}</Table.Td>
      <Table.Td>
        <Text fw={500}>{emp.name}</Text>
      </Table.Td>
      <Table.Td>{emp.manager_name || 'None'}</Table.Td>
      <Table.Td>
        <Group gap="xs">
          {emp.roles?.map((r) => (
            <Badge key={r} size="xs" variant="light">
              {r}
            </Badge>
          ))}
        </Group>
      </Table.Td>
      <Table.Td onClick={(e) => e.stopPropagation()}>
        {isAdmin ? (
          <Button
            size="xs"
            color={emp.is_alive === 1 ? 'green' : 'red'}
            variant="light"
            onClick={() => onToggleStatus(emp.id, emp.is_alive)}
          >
            {emp.is_alive === 1 ? 'Active' : 'Inactive'}
          </Button>
        ) : (
          <Badge color={emp.is_alive === 1 ? 'green' : 'red'}>
            {emp.is_alive === 1 ? 'Active' : 'Inactive'}
          </Badge>
        )}
      </Table.Td>
      { ( isAdmin || isManager ) && (
        <Table.Td>
          <Button
            size="xs"
            variant="light"
            onClick={(e) => { 
              e.stopPropagation(); 
              navigate(`/timelogs/${emp.id}`)
            } }
          >
          </Button>
        </Table.Td>
      )}
    </Table.Tr>
  ));

  return (
    <>
      <Table highlightOnHover withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>User ID</Table.Th>
            <Table.Th>Name</Table.Th>
            <Table.Th>Manager</Table.Th>
            <Table.Th>Roles</Table.Th>
            <Table.Th>Status</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {rows.length > 0 ? (
            rows
          ) : (
            <Table.Tr>
              <Table.Td colSpan={5} align="center">
                No employees found
              </Table.Td>
            </Table.Tr>
          )}
        </Table.Tbody>
      </Table>
    </>
  );
};

export default EmployeeTable;
