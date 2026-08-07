// Role definitions matching backend RoleEnum
export const RoleEnum = Object.freeze({
  ADMIN: 'admin',
  MANAGER: 'manager',
  EMPLOYEE: 'employee',
});

// Project status matching backend StatusEnum
export const StatusEnum = Object.freeze({
  CREATED: 'created',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  ARCHIVED: 'archived',
});

// TimeLog type matching backend TypeEnum
export const TypeEnum = Object.freeze({
  STANDARD: 'standard',
  OVERTIME: 'overtime',
});

// Options for dropdowns and multiselects
export const ROLE_OPTIONS = [
  { value: RoleEnum.ADMIN, label: 'Admin' },
  { value: RoleEnum.MANAGER, label: 'Manager' },
  { value: RoleEnum.EMPLOYEE, label: 'Employee' },
];

export const STATUS_OPTIONS_FOR_MANAGER = [
  { value: StatusEnum.CREATED, label: 'Created' },
  { value: StatusEnum.IN_PROGRESS, label: 'In Progress' },
  { value: StatusEnum.COMPLETED, label: 'Completed' },
]

export const STATUS_OPTIONS = [
  { value: StatusEnum.CREATED, label: 'Created' },
  { value: StatusEnum.IN_PROGRESS, label: 'In Progress' },
  { value: StatusEnum.COMPLETED, label: 'Completed' },
  { value: StatusEnum.ARCHIVED, label: 'Archived' },
];

export const TIMELOG_TYPE_OPTIONS = [
  { value: TypeEnum.STANDARD, label: 'Standard' },
  { value: TypeEnum.OVERTIME, label: 'Overtime' },
];

export const SORT_ORDER_OPTIONS = [
  { value: '-1', label: 'Descending' },
  { value: '1', label: 'Ascending' },
];
