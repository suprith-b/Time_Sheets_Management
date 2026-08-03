import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Title,
  TextInput,
  PasswordInput,
  MultiSelect,
  Select,
  Button,
  Group,
  Stack,
  Alert,
} from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { userService } from '../services/userService';
import { RoleEnum, ROLE_OPTIONS } from '../utils/constants';

const CreateEmployeePage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    userid: '',
    username: '',
    name: '',
    company_mail: '',
    phone_number: '',
    password: '',
    roles: [RoleEnum.EMPLOYEE],
    manager_id: null,
  });

  const [managersList, setManagersList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    userService
      .fetchUsers({ roles: [RoleEnum.MANAGER, RoleEnum.ADMIN] })
      .then(setManagersList)
      .catch(console.error);
  }, []);

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await userService.createUser(formData);
      navigate('/employees');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create employee');
    } finally {
      setLoading(false);
    }
  };

  const managerOptions = managersList.map((m) => ({
    value: String(m.id),
    label: `${m.name} (${m.userid || m.id})`,
  }));

  return (
    <Container size="sm" py="xl">
      <Paper p="xl" withBorder radius="md">
        <Title order={3} mb="lg">
          Create New Employee
        </Title>

        {error && (
          <Alert color="red" mb="md">
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <Stack gap="md">
            <TextInput
              label="User ID"
              placeholder="e.g. EMP001"
              required
              value={formData.userid}
              onChange={(e) => handleChange('userid', e.target.value)}
            />

            <TextInput
              label="Name"
              placeholder="Full Name"
              required
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
            />

            <TextInput
              label="Username"
              placeholder="Username"
              required
              value={formData.username}
              onChange={(e) => handleChange('username', e.target.value)}
            />

            <TextInput
              label="Company Email"
              placeholder="email@company.com"
              required
              value={formData.company_mail}
              onChange={(e) => handleChange('company_mail', e.target.value)}
            />

            <TextInput
              label="Phone Number"
              placeholder="Phone number"
              required
              value={formData.phone_number}
              onChange={(e) => handleChange('phone_number', e.target.value)}
            />

            <PasswordInput
              label="Initial Password"
              placeholder="Set password"
              required
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
            />

            <MultiSelect
              label="Roles"
              data={ROLE_OPTIONS}
              value={formData.roles}
              onChange={(val) => handleChange('roles', val)}
            />

            <Select
              label="Manager"
              placeholder="Select Manager"
              data={managerOptions}
              value={formData.manager_id ? String(formData.manager_id) : null}
              onChange={(val) => handleChange('manager_id', val ? Number(val) : null)}
              searchable
              clearable
            />

            <Group justify="flex-end" mt="md">
              <Button variant="default" onClick={() => navigate('/employees')}>
                Cancel
              </Button>
              <Button type="submit" loading={loading}>
                Create Employee
              </Button>
            </Group>
          </Stack>
        </form>
      </Paper>
    </Container>
  );
};

export default CreateEmployeePage;
