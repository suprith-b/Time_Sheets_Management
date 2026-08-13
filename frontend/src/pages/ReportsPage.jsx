import React, { useState, useEffect } from 'react';
import { Container, Title, Group, Button } from '@mantine/core';
import { IconDownload } from '@tabler/icons-react';
import ReportFilterBar from '../components/ReportFilterBar';
import ReportTable from '../components/ReportTable';
import { analyticsService } from '../services/analyticsService';
import { projectService } from '../services/projectService';
import { useAuth } from '../components/AuthContext';
import { RoleEnum } from '../utils/constants';
import { formatHours } from '../utils/formatters';

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

  const handleExportCsv = () => {
    const headers = ['Employee', 'Project', 'Duration'];
    const rows = (reports || []).map((rep) => [
      rep.name + ' (' + rep.userid + ')' || '',
      rep.project_name || '',
      formatHours(rep.hours),
    ]);

    const csvContent = [
      headers.map((h) => `"${String(h).replace(/"/g, '""')}"`).join(','),
      ...rows.map((row) =>
        row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')
      ),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;

    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const yyyy = today.getFullYear();
    link.setAttribute('download', `reports-${dd}-${mm}-${yyyy}.csv`);

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" align="center" mb="lg">
        <Title order={2} style={{ color: '#0f172a' }}>
          Analytics & Reports
        </Title>
        <Button
          variant="light"
          color="indigo"
          leftSection={<IconDownload size={16} />}
          onClick={handleExportCsv}
        >
          Export CSV
        </Button>
      </Group>

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
