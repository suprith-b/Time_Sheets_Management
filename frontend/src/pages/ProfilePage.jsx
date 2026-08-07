import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
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

const ProfilePage = () => {
  const { userId } = useParams();
  const { user: currentUser, hasRole } = useAuth();

  const targetId = userId ? Number(userId) : currentUser?.id;
  const isAdmin = hasRole(RoleEnum.ADMIN);

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
          roles: [RoleEnum.MANAGER],
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

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="lg">
        {!userId || Number(userId) === currentUser?.id ? 'My Profile' : targetUser.name}
      </Title>
      <ProfileDetailsSection
        targetUser={targetUser}
        userProjects={userProjects}
        managersList={managersList}
        onUpdateSuccess={loadProfile}
      />
    </Container>
  );
};

export default ProfilePage;
