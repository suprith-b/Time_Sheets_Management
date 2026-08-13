import React from 'react';
import { Group, Select, ActionIcon, Textarea } from '@mantine/core';
import { DateTimePicker } from '@mantine/dates';
import { IconTrash } from '@tabler/icons-react';
import { TIMELOG_TYPE_OPTIONS } from '../utils/constants';

const TimesheetRow = ({
  row,
  index,
  projectsList,
  tasksMap,
  onChange,
  onDelete,
  canDelete,
}) => {
  const projectOptions = projectsList.map((p) => ({
    value: String(p.id),
    label: p.name,
  }));

  const availableTasks = row.project_id ? tasksMap[row.project_id] || [] : [];
  const taskOptions = availableTasks.map((t) => ({
    value: String(t.id),
    label: t.name,
  }));

  return (
    <Group wrap="nowrap" align="flex-start" mb="sm">
      <Select
        placeholder="Select Project"
        data={projectOptions}
        value={row.project_id ? String(row.project_id) : null}
        onChange={(val) => onChange(index, 'project_id', val ? Number(val) : null)}
        searchable
        style={{ flex: 2 }}
      />

      <Select
        placeholder="Select Task"
        data={taskOptions}
        value={row.task_id ? String(row.task_id) : null}
        onChange={(val) => onChange(index, 'task_id', val ? Number(val) : null)}
        searchable
        disabled={!row.project_id}
        style={{ flex: 2 }}
      />

      <DateTimePicker
        placeholder="Start Time"
        value={row.start_time ? new Date(row.start_time) : null}
        onChange={(val) => onChange(index, 'start_time', val)}
        style={{ flex: 2 }}
      />

      <DateTimePicker
        placeholder="End Time"
        value={row.end_time ? new Date(row.end_time) : null}
        onChange={(val) => onChange(index, 'end_time', val)}
        style={{ flex: 2 }}
      />

      <Select
        data={TIMELOG_TYPE_OPTIONS}
        value={row.type}
        onChange={(val) => onChange(index, 'type', val)}
        style={{ flex: 1.5 }}
      />

      <Textarea
        placeholder="Comments"
        autosize
        minRows={1}
        maxRows={4}
        value={row.comments || ''}
        onChange={(e) => onChange(index, 'comments', e.target.value)}
        style={{ flex: 2 }}
      />

      <ActionIcon
        color="red"
        variant="subtle"
        disabled={!canDelete}
        onClick={() => onDelete(index)}
        size="lg"
        mt={4}
      >
        <IconTrash size={18} />
      </ActionIcon>
    </Group>
  );
};

export default TimesheetRow;
