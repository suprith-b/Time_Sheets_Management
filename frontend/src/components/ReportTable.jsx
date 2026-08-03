import React from 'react';
import { Table, Text } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { formatHours } from '../utils/formatters';

const ReportTable = ({ reports }) => {
  const navigate = useNavigate();

  const rows = reports.map((rep, idx) => (
    <Table.Tr
      key={`${rep.id}-${rep.project_id}-${idx}`}
      style={{ cursor: 'pointer' }}
      onClick={() => navigate(`/employees/${rep.id}?tab=logs`)}
    >
      <Table.Td>
        <Text fw={500}>{rep.name}</Text>
      </Table.Td>
      <Table.Td>{rep.project_name}</Table.Td>
      <Table.Td>{formatHours(rep.hours)}</Table.Td>
    </Table.Tr>
  ));

  return (
    <Table highlightOnHover withTableBorder>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Employee Name</Table.Th>
          <Table.Th>Project Name</Table.Th>
          <Table.Th>Hours Logged</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.length > 0 ? (
          rows
        ) : (
          <Table.Tr>
            <Table.Td colSpan={3} align="center">
              No report data found
            </Table.Td>
          </Table.Tr>
        )}
      </Table.Tbody>
    </Table>
  );
};

export default ReportTable;
