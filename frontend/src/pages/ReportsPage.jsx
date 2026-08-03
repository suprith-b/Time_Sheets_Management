import React, { useState, useEffect } from 'react';
import { Container, Title } from '@mantine/core';
import ReportFilterBar from '../components/ReportFilterBar';
import ReportTable from '../components/ReportTable';
import { analyticsService } from '../services/analyticsService';
import { userService } from '../services/userService';
import { projectService } from '../services/projectService';
import { useAuth } from '../components/AuthContext';
import { RoleEnum } from '../utils/constants';

const ReportsPage = () => {
  const { hasRole } = useAuth();
  const asRole = hasRole(RoleEnum.ADMIN) ? 'admin' : 'manager';

  const [reports, setReports] = useState([]);
  const [managersList, setManagersList] = useState([]);
  const [projectsList, setProjectsList] = useState([]);

  const [roles, setRoles] = useState([]);
  const [managers, setManagers] = useState([]);
  const [projects, setProjects] = useState([]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [type, setType] = useState(['standard', 'overtime']);
  const [sortBy, setSortBy] = useState('duration');
  const [sortType, setSortType] = useState(-1);

  useEffect(() => {
    userService
      .fetchUsers({ roles: [RoleEnum.MANAGER, RoleEnum.ADMIN] })
      .then(setManagersList)
      .catch(console.error);

    projectService.fetchProjects().then(setProjectsList).catch(console.error);
  }, []);

  const loadReports = async () => {
    try {
      const data = await analyticsService.getReports({
        asRole,
        startDate: startDate ? startDate.toISOString() : null,
        endDate: endDate ? endDate.toISOString() : null,
        projectIds: projects.map(Number),
        type,
        sortBy,
        sortType,
      });
      setReports(data);
    } catch (err) {
      console.error('Failed to fetch report analytics:', err);
    }
  };

  useEffect(() => {
    loadReports();
  }, [asRole, startDate, endDate, projects, type, sortBy, sortType]);

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="lg">
        Analytics & Reports
      </Title>

      <ReportFilterBar
        roles={roles}
        setRoles={setRoles}
        managers={managers}
        setManagers={setManagers}
        managersList={managersList}
        projects={projects}
        setProjects={setProjects}
        projectsList={projectsList}
        startDate={startDate}
        setStartDate={setStartDate}
        endDate={endDate}
        setEndDate={setEndDate}
        type={type}
        setType={setType}
        sortBy={sortBy}
        setSortBy={setSortBy}
        sortType={sortType}
        setSortType={setSortType}
      />

      <ReportTable reports={reports} />
    </Container>
  );
};

export default ReportsPage;
