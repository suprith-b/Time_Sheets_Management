import dayjs from 'dayjs';

export const formatDate = (dateValue, format = 'DD MMM YYYY') => {
  if (!dateValue) return '—';
  return dayjs(dateValue).format(format);
};

export const formatDateTime = (dateValue, format = 'DD MMM YYYY HH:mm') => {
  if (!dateValue) return '—';
  return dayjs(dateValue).format(format);
};

export const formatHours = (hours) => {
  if (hours == null) return '—';
  return `${Number(hours).toFixed(1)} hrs`;
};
