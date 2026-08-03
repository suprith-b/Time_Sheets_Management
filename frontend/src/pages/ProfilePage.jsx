import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Tabs,
  Title,
  Loader,
  Center,
  Text,
} from '@mantine/core';
import { useAuth } from '../components/AuthContext';
import { userService } from '../services/userService';
import { projectService } from '../services/projectService';
import { RoleEnum } from '../utils/constants';
import ProfileDetailsSection from '../components/ProfileDetailsSection';
import ProfileLogsSection from '../components/ProfileLogsSection';

const ProfilePage = () => {
  const { userId } = useParams();
  const { user: currentUser, hasRole } = useAuth();

  const targetId = userId ? Number(userId) : currentUser?.id;
  const isAdmin = hasRole(RoleEnum.ADMIN);
  const isSelf = !userId || Number(userId) === currentUser?.id;

  const [targetUser, setTargetUser] = useState(null);
  const [managersList, setManagersList] = useState([]);
  const [userProjects, setUserProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadProfile = async () => {
    if (!targetId) return;
    setLoading(true);
    try {
      const [userData, projects] = await Promise.all([
        userService.getUserById(targetId),
        projectService.fetchUserProjects(targetId),
      ]);
      setTargetUser(userData);
      setUserProjects(projects);

      if (isAdmin) {
        const mgrs = await userService.fetchUsers({
          roles: [RoleEnum.MANAGER, RoleEnum.ADMIN],
        });
        setManagersList(mgrs);
      }
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, [targetId]);

  if (loading) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (!targetUser) {
    return (
      <Center py="xl">
        <Text c="dimmed">Unable to load profile.</Text>
      </Center>
    );
  }

  const canSeeLogs = isSelf || isAdmin || hasRole(RoleEnum.MANAGER);

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="lg">
        {isSelf ? 'My Profile' : targetUser.name}
      </Title>

      <Tabs defaultValue="details">
        <Tabs.List mb="md">
          <Tabs.Tab value="details">Details</Tabs.Tab>
          {canSeeLogs && <Tabs.Tab value="logs">Time Logs</Tabs.Tab>}
        </Tabs.List>

        <Tabs.Panel value="details">
          <ProfileDetailsSection
            targetUser={targetUser}
            userProjects={userProjects}
            managersList={managersList}
            onUpdateSuccess={loadProfile}
          />
        </Tabs.Panel>

        {canSeeLogs && (
          <Tabs.Panel value="logs">
            <ProfileLogsSection userId={targetId} />
          </Tabs.Panel>
        )}
      </Tabs>
    </Container>
  );
};

export default ProfilePage;
