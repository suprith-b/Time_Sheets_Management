import React, { useState, useEffect } from 'react';
import { Container, Title, Group, Button } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import { RoleEnum } from '../utils/constants';
import EmployeeFilterBar from '../components/EmployeeFilterBar';
import LogsSection from '../components/LogsSection';
import EmployeeTable from '../components/EmployeeTable';
import { userService } from '../services/userService';
import { projectService } from '../services/projectService';

const EmployeesPage = () => {
  const navigate = useNavigate();
  const { hasRole } = useAuth();
  const isAdmin = hasRole(RoleEnum.ADMIN);

  const [employees, setEmployees] = useState([]);
  const [managersList, setManagersList] = useState([]);
  const [projectsList, setProjectsList] = useState([]);

  const [ showTimeLogs, setShowTimeLogs ] = useState(null)

  const [search, setSearch] = useState('');
  const [roles, setRoles] = useState([]);
  const [managerId, setManagerId] = useState(null);
  const [status, setStatus] = useState(['1']);
  const [projects, setProjects] = useState([]);
  const [hasManager, setHasManager] = useState(['1']);

  const loadFilterOptions = async () => {
    try {
      const mgrs = await userService.fetchUsers({
        roles: [RoleEnum.MANAGER, RoleEnum.ADMIN],
      });
      setManagersList(mgrs);

      const projs = await projectService.fetchProjects();
      setProjectsList(projs);
    } catch (err) {
      console.error('Failed to load filter options:', err);
    }
  };

  const loadEmployees = async () => {
    try {
      const data = await userService.fetchUsers({
        roles: roles.length > 0 ? roles : undefined,
        managerId,
        isAlive: status.map(Number),
        projectIds: projects.map(Number),
        hasManager: hasManager.map(Number),
      });
      setEmployees(data);
    } catch (err) {
      console.error('Failed to fetch employees:', err);
    }
  };

  useEffect(() => {
    loadFilterOptions();
  }, []);

  useEffect(() => {
    loadEmployees();
  }, [roles, managerId, status, projects, hasManager]);

  const handleToggleStatus = async (userId, currentIsAlive) => {
    try {
      await userService.toggleUserStatus(userId, currentIsAlive);
      loadEmployees();
    } catch (err) {
      console.error('Failed to toggle status:', err);
    }
  };

  const filteredEmployees = employees.filter((emp) =>
    emp.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" mb="lg">
        <Title order={2}>Employees</Title>
        {isAdmin && (
          <Button
            leftSection={<IconPlus size={16} />}
            onClick={() => navigate('/employees/new')}
          >
            Add Employee
          </Button>
        )}
      </Group>

      <EmployeeFilterBar
        search={search}
        setSearch={setSearch}
        roles={roles}
        setRoles={setRoles}
        managerId={managerId}
        setManagerId={setManagerId}
        managersList={managersList}
        status={status}
        setStatus={setStatus}
        projects={projects}
        setProjects={setProjects}
        projectsList={projectsList}
        hasManager={hasManager}
        setHasManager={setHasManager}
      />
      <EmployeeTable
        employees={filteredEmployees}
        onToggleStatus={handleToggleStatus}
        setShowTimeLogs={setShowTimeLogs}
      />
    </Container>
  );
};

export default EmployeesPage;
