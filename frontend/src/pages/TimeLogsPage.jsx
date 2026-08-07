import React from 'react';
import { Container, Title } from '@mantine/core';
import { useAuth } from '../components/AuthContext';
import LogsSection from '../components/LogsSection';

const TimeLogsPage = () => {
  const { user: currentUser } = useAuth();

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="lg">
        Time Logs
      </Title>
      <LogsSection userId={currentUser?.id} />
    </Container>
  );
};

export default TimeLogsPage;
