import React, { useState, useEffect } from 'react';
import { Container, Title, Group, Button } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import { RoleEnum } from '../utils/constants';
import ProjectFilterBar from '../components/ProjectFilterBar';
import ProjectTable from '../components/ProjectTable';
import { projectService } from '../services/projectService';

const ProjectsPage = () => {
  const navigate = useNavigate();
  const { user, hasRole, isOneOfRoles } = useAuth();
  const isAdmin = hasRole(RoleEnum.ADMIN);

  const [projects, setProjects] = useState([]);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState(['in_progress']);
  const [sortBy, setSortBy] = useState('duration');
  const [sortType, setSortType] = useState(-1);

  const loadProjects = async () => {
    try {
      let data = [];
      if (isAdmin) {
        data = await projectService.fetchProjects({ status, sortBy, sortType });
      } else {
        data = await projectService.fetchUserProjects(user.id, {
          status,
          sortBy,
          sortType,
        });
      }
      setProjects(data);
    } catch (err) {
      console.error('Failed to load projects:', err);
    }
  };

  useEffect(() => {
    loadProjects();
  }, [status, sortBy, sortType]);

  const handleStatusChange = async (projectId, newStatus) => {
    try {
      await projectService.updateProject(projectId, { status: newStatus });
      loadProjects();
    } catch (err) {
      console.error('Failed to update project status:', err);
    }
  };

  const filteredProjects = projects.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" align="center" mb="lg">
        <Title order={2} style={{ color: '#0f172a' }}>
          Projects
        </Title>
        {isAdmin && (
          <Button
            leftSection={<IconPlus size={16} />}
            variant="filled"
            color="indigo"
            onClick={() => navigate('/projects/new')}
          >
            Add Project
          </Button>
        )}
      </Group>

      <ProjectFilterBar
        search={search}
        setSearch={setSearch}
        status={status}
        setStatus={setStatus}
        sortBy={sortBy}
        setSortBy={setSortBy}
        sortType={sortType}
        setSortType={setSortType}
      />

      <ProjectTable
        projects={filteredProjects}
        onStatusChange={handleStatusChange}
      />
    </Container>
  );
};

export default ProjectsPage;
