import React, { useState } from 'react';
import { Container, Paper, Title, TextInput, PasswordInput, Button, Alert, Text } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(email, password);
      navigate('/timesheet');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password');
    }
  };

  return (
    <Container size={420} my={80}>
      <Title align="center" fw={900}>
        Timesheets Portal
      </Title>
      <Text c="dimmed" size="sm" align="center" mt={5} mb={30}>
        Sign in with your company credentials
      </Text>

      <Paper withBorder shadow="md" p={30} radius="md">
        {error && (
          <Alert color="red" mb="md">
            {error}
          </Alert>
        )}
        <form onSubmit={handleSubmit}>
          <TextInput
            label="Company Email"
            placeholder="your@email.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            mb="md"
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            mb="xl"
          />
          <Button type="submit" fullWidth loading={loading}>
            Sign In
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default LoginPage;
