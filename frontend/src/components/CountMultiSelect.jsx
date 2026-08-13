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
import { IconChevronDown, IconSearch, IconX } from '@tabler/icons-react';

const CountMultiSelect = ({
  label,
  placeholder = 'Select...',
  data = [],
  value = [],
  onChange,
  searchable = false,
  disabled = false,
  style = {},
}) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

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
    if (disabled) return;
    if (value.includes(val)) {
      onChange(value.filter((v) => v !== val));
    } else {
      onChange([...value, val]);
    }
  };

  const selectedItem =
    value.length === 1 ? data.find((d) => d.value === value[0]) : null;

  const triggerLabel =
    value.length === 0
      ? placeholder
      : value.length === 1 && selectedItem
      ? selectedItem.label
      : `${value.length} selected`;

  return (
    <Box style={{ position: 'relative', minWidth: 130, ...style }} ref={ref}>
      {label && (
        <Text size="xs" fw={600} mb={4} c="dimmed" style={{ textTransform: 'uppercase', letterSpacing: '0.04em' }}>
          {label}
        </Text>
      )}

      <UnstyledButton
        onClick={() => !disabled && setOpen((o) => !o)}
        disabled={disabled}
        style={{
          width: '100%',
          height: '36px',
          border: disabled ? '1px solid #e2e8f0' : open ? '1px solid #6366f1' : '1px solid #cbd5e1',
          borderRadius: '8px',
          padding: '0 10px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: disabled ? '#f1f5f9' : '#ffffff',
          cursor: disabled ? 'not-allowed' : 'pointer',
          boxShadow: open && !disabled ? '0 0 0 3px rgba(99, 102, 241, 0.15)' : 'none',
          transition: 'all 0.15s ease',
        }}
      >
        <Group gap="xs" style={{ overflow: 'hidden', flex: 1 }} wrap="nowrap">
          <Text
            size="xs"
            truncate
            fw={value.length > 0 ? 500 : 400}
            style={{ color: value.length === 0 ? (disabled ? '#64748b' : '#94a3b8') : '#0f172a' }}
          >
            {triggerLabel}
          </Text>
          {value.length > 1 && (
            <Badge size="xs" variant="filled" color="indigo" radius="xl">
              {value.length}
            </Badge>
          )}
        </Group>
        <IconChevronDown size={14} style={{ color: '#64748b', transition: 'transform 0.15s ease', transform: open ? 'rotate(180deg)' : 'none' }} />
      </UnstyledButton>

      {open && !disabled && (
        <Paper
          shadow="md"
          withBorder
          radius="md"
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            minWidth: '200px',
            maxWidth: '280px',
            zIndex: 300,
            marginTop: 4,
            backgroundColor: '#ffffff',
            borderColor: '#e2e8f0',
          }}
        >
          {searchable && (
            <Box p="xs" style={{ borderBottom: '1px solid #f1f5f9' }}>
              <TextInput
                placeholder="Search..."
                leftSection={<IconSearch size={14} />}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                size="xs"
                radius="sm"
                autoFocus
              />
            </Box>
          )}

          <ScrollArea.Autosize mah={200}>
            <Box p="xs">
              {filtered.length === 0 ? (
                <Text size="xs" c="dimmed" ta="center" py="xs">
                  No options found
                </Text>
              ) : (
                filtered.map((item) => (
                  <Box
                    key={item.value}
                    onClick={() => toggle(item.value)}
                    style={{
                      padding: '5px 8px',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      backgroundColor: value.includes(item.value) ? '#eef2ff' : 'transparent',
                      transition: 'all 0.1s ease',
                    }}
                  >
                    <Checkbox
                      label={item.label}
                      checked={value.includes(item.value)}
                      onChange={() => {}}
                      size="xs"
                      color="indigo"
                      radius="sm"
                      style={{ pointerEvents: 'none', width: '100%' }}
                    />
                  </Box>
                ))
              )}
            </Box>
          </ScrollArea.Autosize>

          {value.length > 0 && (
            <Box
              p="xs"
              style={{
                borderTop: '1px solid #f1f5f9',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backgroundColor: '#f8fafc',
                borderBottomLeftRadius: '8px',
                borderBottomRightRadius: '8px',
              }}
            >
              <Text size="xs" c="dimmed">
                {value.length} selected
              </Text>
              <UnstyledButton
                onClick={() => onChange([])}
                style={{
                  cursor: 'pointer',
                  color: '#ef4444',
                  fontSize: '11px',
                  fontWeight: 500,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '3px',
                }}
              >
                <IconX size={12} /> Clear
              </UnstyledButton>
            </Box>
          )}
        </Paper>
      )}
    </Box>
  );
};

export default CountMultiSelect;
