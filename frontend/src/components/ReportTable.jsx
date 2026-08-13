import React from 'react';
import { Table, Text, Button } from '@mantine/core';
import { IconClock } from '@tabler/icons-react';
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
        <Text fw={600} c="dark">{rep.name} ({rep.userid})</Text>
      </Table.Td>
      <Table.Td>{rep.project_name}</Table.Td>
      <Table.Td>{formatHours(rep.hours)}</Table.Td>
      <Table.Td>
        <Button
          size="xs"
          variant="light"
          color="gray"
          leftSection={<IconClock size={14} />}
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/timelogs/${rep.id}`);
          }}
        >
          View Logs
        </Button>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Table highlightOnHover withTableBorder>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Employee</Table.Th>
          <Table.Th>Project</Table.Th>
          <Table.Th>Duration</Table.Th>
          <Table.Th>Actions</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.length > 0 ? (
          rows
        ) : (
          <Table.Tr>
            <Table.Td colSpan={4} align="center">
              No report data found
            </Table.Td>
          </Table.Tr>
        )}
      </Table.Tbody>
    </Table>
  );
};

export default ReportTable;
