import React, { useState, useEffect } from 'react';
import { Container, Title } from '@mantine/core';
import ReportFilterBar from '../components/ReportFilterBar';
import ReportTable from '../components/ReportTable';
import { analyticsService } from '../services/analyticsService';
import { projectService } from '../services/projectService';
import { useAuth } from '../components/AuthContext';
import { RoleEnum } from '../utils/constants';

const ReportsPage = () => {
  const { user: currentUser } = useAuth();

  const [reports, setReports] = useState([]);
  const [projectsList, setProjectsList] = useState([]);

  const getInitialViewAs = (user) => {
    const rawRoles = user?.roles || [];
    const normalized = rawRoles.map((r) => String(r).toLowerCase());
    const matched = [];
    if (normalized.includes('admin')) matched.push(RoleEnum.ADMIN);
    if (normalized.includes('manager')) matched.push(RoleEnum.MANAGER);
    return matched.length > 0 ? matched : [RoleEnum.ADMIN, RoleEnum.MANAGER];
  };

  const [viewAs, setViewAs] = useState(() => getInitialViewAs(currentUser));
  const [projects, setProjects] = useState([]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [type, setType] = useState(['standard', 'overtime']);
  const [sortBy, setSortBy] = useState('duration');
  const [sortType, setSortType] = useState(-1);

  useEffect(() => {
    projectService.fetchProjects().then(setProjectsList).catch(console.error);
  }, []);

  useEffect(() => {
    if (currentUser?.roles) {
      const initial = getInitialViewAs(currentUser);
      if (initial.length > 0 && viewAs.length === 0) {
        setViewAs(initial);
      }
    }
  }, [currentUser]);

  const loadReports = async () => {
    try {
      const data = await analyticsService.getReports({
        viewAs,
        startDate: startDate ? new Date(startDate).toISOString() : null,
        endDate: endDate ? new Date(endDate).toISOString() : null,
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
  }, [viewAs, startDate, endDate, projects, type, sortBy, sortType]);

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="lg">
        Analytics & Reports
      </Title>

      <ReportFilterBar
        viewAs={viewAs}
        setViewAs={setViewAs}
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
