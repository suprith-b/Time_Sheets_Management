import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Text,
  Checkbox,
  Paper,
  ScrollArea,
  TextInput,
  Badge,
  Group,
  UnstyledButton,
} from '@mantine/core';
import { IconChevronDown, IconSearch } from '@tabler/icons-react';

/**
 * A multiselect that shows "N selected" as the trigger instead of chips.
 * Expands a dropdown when clicked. Supports searchable list.
 *
 * Props:
 *  - label: string
 *  - placeholder: string (shown when nothing selected)
 *  - data: { value, label }[]
 *  - value: string[]
 *  - onChange: (string[]) => void
 *  - searchable: boolean
 */
const CountMultiSelect = ({
  label,
  placeholder = 'Select...',
  data = [],
  value = [],
  onChange,
  searchable = false,
}) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  // Close when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
        setSearch('');
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const filtered = searchable
    ? data.filter((d) => d.label.toLowerCase().includes(search.toLowerCase()))
    : data;

  const toggle = (val) => {
    if (value.includes(val)) {
      onChange(value.filter((v) => v !== val));
    } else {
      onChange([...value, val]);
    }
  };

  const triggerLabel =
    value.length === 0
      ? placeholder
      : `${value.length} selected`;

  return (
    <Box style={{ position: 'relative', flex: 1 }} ref={ref}>
      {label && (
        <Text size="sm" fw={500} mb={4}>
          {label}
        </Text>
      )}

      <UnstyledButton
        onClick={() => setOpen((o) => !o)}
        style={{
          width: '100%',
          border: '1px solid var(--mantine-color-gray-4)',
          borderRadius: 'var(--mantine-radius-sm)',
          padding: '6px 10px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: 'var(--mantine-color-white)',
          cursor: 'pointer',
        }}
      >
        <Text size="sm" c={value.length === 0 ? 'dimmed' : 'dark'}>
          {triggerLabel}
        </Text>
        <IconChevronDown size={14} />
      </UnstyledButton>

      {open && (
        <Paper
          shadow="md"
          withBorder
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            zIndex: 200,
            marginTop: 4,
          }}
        >
          {searchable && (
            <Box p="xs" pb={0}>
              <TextInput
                placeholder="Search..."
                leftSection={<IconSearch size={14} />}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                size="xs"
                autoFocus
              />
            </Box>
          )}

          <ScrollArea.Autosize mah={200}>
            <Box p="xs">
              {filtered.length === 0 ? (
                <Text size="sm" c="dimmed" ta="center" py="xs">
                  No options
                </Text>
              ) : (
                filtered.map((item) => (
                  <Checkbox
                    key={item.value}
                    label={item.label}
                    checked={value.includes(item.value)}
                    onChange={() => toggle(item.value)}
                    mb="xs"
                    size="sm"
                  />
                ))
              )}
            </Box>
          </ScrollArea.Autosize>

          {value.length > 0 && (
            <Box
              px="xs"
              pb="xs"
              style={{ borderTop: '1px solid var(--mantine-color-gray-2)' }}
            >
              <UnstyledButton onClick={() => onChange([])} style={{ cursor: 'pointer' }}>
                <Text size="xs" c="dimmed">
                  Clear all
                </Text>
              </UnstyledButton>
            </Box>
          )}
        </Paper>
      )}
    </Box>
  );
};

export default CountMultiSelect;
