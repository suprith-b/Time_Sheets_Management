import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import AppHeader from './components/AppHeader';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import EmployeesPage from './pages/EmployeesPage';
import CreateEmployeePage from './pages/CreateEmployeePage';
import ProjectsPage from './pages/ProjectsPage';
import ProjectDetailPage from './pages/ProjectDetailPage';
import CreateProjectPage from './pages/CreateProjectPage';
import ReportsPage from './pages/ReportsPage';
import EnterTimesheetPage from './pages/EnterTimesheetPage';
import { RoleEnum } from './utils/constants';

function App() {
  return (
    <>
      <AppHeader />
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/profile" element={<ProfilePage />} />
        </Route>

        <Route
          element={
            <ProtectedRoute allowedRoles={[RoleEnum.ADMIN, RoleEnum.MANAGER]} />
          }
        >
          <Route path="/employees" element={<EmployeesPage />} />
          <Route path="/employees/:userId" element={<ProfilePage />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={[RoleEnum.ADMIN]} />}>
          <Route path="/employees/new" element={<CreateEmployeePage />} />
          <Route path="/projects/new" element={<CreateProjectPage />} />
        </Route>

        <Route
          element={
            <ProtectedRoute
              allowedRoles={[RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.EMPLOYEE]}
            />
          }
        >
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
        </Route>

        <Route
          element={
            <ProtectedRoute allowedRoles={[RoleEnum.ADMIN, RoleEnum.MANAGER]} />
          }
        >
          <Route path="/reports" element={<ReportsPage />} />
        </Route>

        <Route
          element={
            <ProtectedRoute allowedRoles={[RoleEnum.EMPLOYEE, RoleEnum.ADMIN]} />
          }
        >
          <Route path="/timesheet" element={<EnterTimesheetPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/profile" replace />} />
      </Routes>
    </>
  );
}

export default App;
