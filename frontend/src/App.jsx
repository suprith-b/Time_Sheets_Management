import { useEffect, useMemo, useState } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/admin'

const adminNav = [
  ['dashboard', 'chart', 'Dashboard'],
  ['projects', 'grid', 'Manage Projects'],
  ['managers', 'user', 'Managers'],
  ['employees', 'user', 'Manage Employees'],
  ['reports', 'chart', 'Reports'],
]
const managerNav = [
  ['manager-dashboard', 'chart', 'Dashboard'],
  ['manager-timesheet', 'edit', 'New Timesheet'],
  ['manager-history', 'chart', 'Work History'],
  ['team-assignment', 'user', 'Team Assignment'],
  ['reports', 'chart', 'Reports'],
  ['projects', 'grid', 'Projects & Tasks'],
]
const employeeNav = [
  ['employee-timesheet', 'edit', 'New Timesheet'],
  ['employee-history', 'chart', 'Work History'],
]

const formatHours = value => `${Number(value || 0).toFixed(2).replace(/\.00$/, '')}h`
const today = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' }).format(new Date())
const readImage = file => new Promise((resolve, reject) => {
  if (!file || !file.size) return resolve(null)
  const reader = new FileReader()
  reader.onload = () => resolve(reader.result)
  reader.onerror = () => reject(new Error('Could not read selected image.'))
  reader.readAsDataURL(file)
})

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (response.status === 204) return null
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map(item => item.msg).join(', ') : data.detail
    throw new Error(detail || 'Request failed.')
  }
  return data
}

function Icon({ name }) {
  const paths = {
    user: 'M20 21a8 8 0 0 0-16 0M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z',
    grid: 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z',
    chart: 'M4 19V5M4 19h16M8 16v-5M13 16V8M18 16v-8',
    plus: 'M12 5v14M5 12h14',
    trash: 'M4 7h16M10 11v6M14 11v6M6 7l1 14h10l1-14M9 7V4h6v3',
    edit: 'M4 20h4l10-10-4-4L4 16v4ZM13 7l4 4',
    close: 'M6 6l12 12M18 6 6 18',
    logo: 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z',
  }
  return <svg aria-hidden="true" className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d={paths[name]} /></svg>
}

function Badge({ value }) {
  const colors = {
    employee: 'bg-cyan-950 text-cyan-400',
    manager: 'bg-amber-950 text-amber-400',
    admin: 'bg-rose-950 text-rose-400',
    created: 'bg-slate-700 text-slate-300',
    in_progress: 'bg-blue-950 text-blue-400',
    completed: 'bg-emerald-950 text-emerald-400',
    active: 'bg-emerald-950 text-emerald-400',
    inactive: 'bg-rose-950 text-rose-400',
  }
  return <span className={`rounded px-2 py-1 text-xs font-bold uppercase ${colors[value] || 'bg-slate-700 text-slate-300'}`}>{String(value || '').replace('_', ' ')}</span>
}

function Sidebar({ page, setPage, role, setRole }) {
  const switchRole = nextRole => {
    setRole(nextRole)
    setPage(
      nextRole === 'Admin'
        ? 'dashboard'
        : nextRole === 'Employee'
        ? 'employee-timesheet'
        : 'manager-dashboard'
    )
  }
  const nav = role === 'Employee' ? employeeNav : role === 'Manager' ? managerNav : adminNav
  return <aside className="flex min-h-screen w-80 shrink-0 flex-col border-r border-slate-800 bg-[#0e131d] max-lg:w-72 max-md:hidden">
    <div className="flex items-center gap-3 border-b border-slate-800 px-5 py-6">
      <span className="grid h-9 w-9 place-items-center rounded-lg bg-blue-500 text-white"><Icon name="logo" /></span>
      <div><b className="block text-xl leading-5">TimeSheet</b><small className="text-blue-300">Management System</small></div>
    </div>
    <div className="border-b border-slate-800 p-5">
      <p className="mb-3 text-xs font-bold uppercase tracking-widest text-blue-200">Viewing as</p>
      {['Employee', 'Manager', 'Admin'].map(item => <button key={item} onClick={() => switchRole(item)} className={`mb-1 flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-lg ${role === item ? 'bg-blue-500/15 font-semibold text-blue-400' : 'text-blue-200/80'}`}><span className="h-2 w-2 rounded-full bg-current opacity-80" />{item}</button>)}
    </div>
    <nav className="p-5">
      <p className="mb-3 text-xs font-bold uppercase tracking-widest text-blue-200">{role === 'Employee' || role === 'Manager' ? 'My Work' : role}</p>
      {nav.map(([key, icon, label]) => <button key={key} onClick={() => setPage(key)} className={`mb-2 flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-lg ${page === key ? 'bg-slate-800 text-white' : 'text-blue-200/80 hover:bg-slate-800/60'}`}><span className="text-blue-400"><Icon name={icon} /></span>{label}</button>)}
      <p className="mb-3 mt-8 text-xs font-bold uppercase tracking-widest text-blue-200">Account</p>
      <button onClick={() => setPage('profile')} className={`flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-lg ${page === 'profile' ? 'bg-slate-800 text-white' : 'text-blue-200/80 hover:bg-slate-800/60'}`}><span className="text-blue-400"><Icon name="user" /></span>Profile</button>
    </nav>
    <div className="mt-auto flex items-center gap-3 border-t border-slate-800 p-5"><span className="grid h-9 w-9 place-items-center rounded-full border border-blue-700 bg-blue-950 text-xs text-blue-300">{role === 'Admin' ? 'AU' : role === 'Employee' ? 'EM' : 'MG'}</span><div><b className="block text-sm">{role} User</b><small className="text-blue-200/80">{role}</small></div></div>
  </aside>
}

function Header({ page, role }) {
  const labels = { dashboard: 'Admin Dashboard', employees: 'Manage Employees', managers: 'Managers', projects: 'Manage Projects', reports: 'Reports', profile: 'Profile', 'employee-timesheet': 'New Timesheet', 'employee-history': 'Work History', 'manager-timesheet': 'New Timesheet', 'manager-history': 'Work History', 'team-assignment': 'Team Assignment' }
  return <header className="flex h-14 items-center justify-between border-b border-slate-800 px-5 md:px-8">
    <div className="text-lg"><span className="text-slate-400">{role}</span> <span className="mx-1 text-slate-600">›</span> <b>{labels[page]}</b></div>
    <div className="font-mono text-sm text-slate-400">{today} <span className="mx-2 border-l border-slate-700" />v2.4.1</div>
  </header>
}
function Dashboard() {
  const [data, setData] = useState(null)
  const [reports, setReports] = useState([])
  const [error, setError] = useState('')
  const [range, setRange] = useState({ start: '2026-06-20', end: '2026-06-24' })
  const [appliedRange, setAppliedRange] = useState({ start: '2026-06-20', end: '2026-06-24' })

  useEffect(() => {
    api('/dashboard')
      .then(setData)
      .catch(error => setError(error.message))
  }, [])

  useEffect(() => {
    const params = new URLSearchParams({ start_date: appliedRange.start, end_date: appliedRange.end })
    api(`/reports?${params}`)
      .then(setReports)
      .catch(error => setError(error.message))
  }, [appliedRange])

  if (error) return <><PageTitle title="Admin Dashboard" subtitle="Overview of all projects, managers and employees" /><Empty message={error} /></>
  if (!data) return <Loading />

  const projects = data.projects
  const managers = data.team_workload
  const visibleReports = reports
  const totalProjects = data.statistics.total_projects || 0
  const totalManagers = data.statistics.total_managers || 0
  const totalEmployees = data.statistics.total_employees || 0
  const totalTasks = projects.reduce((total, project) => total + Number(project.task_count || 0), 0)
  const completed = projects.filter(project => project.status === 'completed').length
  const inProgress = projects.filter(project => project.status === 'in_progress').length
  const inactive = projects.filter(project => project.active_status === 'inactive').length
  const progress = Math.round((completed / Math.max(projects.length, 1)) * 100)
  const stats = [
    ['Projects', totalProjects, `${projects.filter(project => project.active_status !== 'inactive').length} Active`, 'grid', 'text-violet-400', 'bg-violet-500'],
    ['Managers', totalManagers, `${managers.reduce((total, manager) => total + Number(manager.team_size || 0), 0)} Assigned employees`, 'user', 'text-blue-400', 'bg-blue-500'],
    ['Employees', totalEmployees, `${data.attention.unassigned_employees || 0} Unassigned`, 'user', 'text-emerald-400', 'bg-emerald-500'],
    ['Tasks', totalTasks, `${data.attention.projects_due_within_seven_days || 0} Due soon`, 'chart', 'text-orange-400', 'bg-orange-500'],
    ['Overall Progress', `${progress}%`, 'Completed projects', 'chart', 'text-rose-400', 'bg-rose-500'],
  ]
  const projectCounts = [
    ['completed', completed, 'bg-emerald-500'],
    ['in_progress', inProgress, 'bg-blue-500'],
    ['created', projects.filter(project => project.status === 'created').length, 'bg-orange-400'],
    ['inactive', inactive, 'bg-rose-500'],
  ]
  const maxManagerHours = Math.max(...managers.map(manager => Number(manager.hours_logged || manager.team_size || 1)), 1)
  const rangeLabel = `${new Date(appliedRange.start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${new Date(appliedRange.end).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
  const applyRange = () => setAppliedRange(range)

  return <>
    <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div><h1 className="text-3xl font-black tracking-tight">Admin Dashboard</h1><p className="text-blue-200/80">Overview of all projects, managers and employees Â· {rangeLabel}</p></div>
      <div className="flex flex-wrap items-center gap-2 rounded-lg border border-slate-700 bg-[#101620] px-3 py-2 text-sm text-blue-100"><span className="text-blue-400"><Icon name="chart" /></span><input aria-label="Start date" type="date" className="control w-36 px-2 py-1 text-xs" value={range.start} onChange={event => setRange({ ...range, start: event.target.value })} /><span className="text-slate-500">to</span><input aria-label="End date" type="date" className="control w-36 px-2 py-1 text-xs" value={range.end} onChange={event => setRange({ ...range, end: event.target.value })} /><button className="btn-primary px-3 py-1.5 text-xs" onClick={applyRange}>Apply</button><button className="btn-secondary px-3 py-1.5 text-xs" onClick={() => { const next = { start: '2026-06-20', end: '2026-06-24' }; setRange(next); setAppliedRange(next) }}>This Week</button></div>
    </div>
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">{stats.map(([label, value, text, icon, color, bar]) => <div className="panel p-4" key={label}><div className="flex items-center gap-4"><span className={`grid h-12 w-12 place-items-center rounded-lg bg-white/5 ${color}`}><Icon name={icon} /></span><div><b className="block text-2xl text-white">{value}</b><p className="text-sm font-semibold text-slate-300">{label}</p><small className="text-blue-200/70">{text}</small></div></div><div className="mt-3 h-1.5 rounded bg-slate-800"><span className={`block h-full rounded ${bar}`} style={{ width: label === 'Overall Progress' ? `${progress}%` : '64%' }} /></div></div>)}</div>
    <div className="mt-4 grid gap-4 xl:grid-cols-12">
      <section className="panel p-5 xl:col-span-4"><h2 className="font-bold">Projects Overview</h2><div className="mt-5 flex items-center gap-6"><div className="grid h-36 w-36 place-items-center rounded-full border-[18px] border-blue-500 border-b-orange-400 border-l-rose-400 border-r-emerald-500"><div className="text-center"><b className="block text-3xl">{totalProjects}</b><small>Total Projects</small></div></div><div className="w-full space-y-3 text-sm">{projectCounts.map(([status, count, color]) => <div key={status}><div className="mb-1 flex items-center justify-between"><span className="flex items-center gap-2"><i className={`h-2.5 w-2.5 rounded-full ${color}`} />{status.replace('_', ' ')}</span><b>{count}</b></div><div className="h-1.5 rounded bg-slate-800"><span className={`block h-full rounded ${color}`} style={{ width: `${Math.round((count / Math.max(totalProjects, 1)) * 100)}%` }} /></div></div>)}</div></div></section>
      <section className="panel p-5 xl:col-span-5"><h2 className="font-bold">Projects by Manager</h2><div className="mt-5 flex h-48 items-end gap-5">{managers.slice(0, 4).map(manager => { const value = Number(manager.hours_logged || manager.team_size || 1); return <div className="flex flex-1 flex-col items-center gap-2" key={manager.manager_id}><span className="grid h-10 w-10 place-items-center rounded-full border border-blue-700 bg-blue-950 text-xs font-bold text-blue-300">{manager.manager_name.split(' ').map(word => word[0]).join('').slice(0, 2)}</span><b className="text-sm">{manager.team_size || Math.round(value / 8)}</b><span className="w-full rounded-t-md bg-blue-500 shadow-[0_0_20px_rgba(59,130,246,.25)]" style={{ height: `${Math.max(24, (value / maxManagerHours) * 120)}px` }} /><small className="text-center text-blue-200/70">{manager.manager_name}</small></div> })}</div></section>
      <section className="panel p-5 xl:col-span-3"><h2 className="font-bold">Recent Activity</h2><div className="mt-3 divide-y divide-slate-800">{data.recent_activity?.length ? data.recent_activity.slice(0, 5).map(item => <div className="flex items-center justify-between gap-3 py-3 text-sm" key={item.id}><span className="min-w-0 truncate">{item.message}</span><span className="shrink-0 text-blue-200/60">{item.created_at}</span></div>) : <p className="py-8 text-sm text-slate-400">No activity records are stored in the current database schema.</p>}</div></section>
    </div>
    <div className="mt-4 grid gap-4 xl:grid-cols-12">
      <section className="panel overflow-hidden xl:col-span-8">
        <div className="flex flex-wrap items-center justify-between gap-3 px-5 py-4"><div><h2 className="font-bold">Timesheet Approvals</h2><p className="text-sm text-blue-200/70">Approval workflow is not stored in the current database schema.</p></div><div className="flex gap-2 text-xs"><span className="rounded bg-slate-800 px-2 py-1 text-slate-300">0 approved</span><span className="rounded bg-rose-950 px-2 py-1 text-rose-300">0 rejected</span></div></div>
        <p className="border-t border-slate-800 px-5 py-8 text-sm text-slate-400">No approval records are stored in the current database schema.</p>
      </section>
      <section className="panel p-5 xl:col-span-4"><h2 className="font-bold">Team Capacity</h2><div className="mt-5 space-y-4">{managers.length ? managers.slice(0, 4).map(manager => { const value = Math.min(100, Number(manager.team_size || 0) * 20); return <div key={manager.manager_id}><div className="mb-1 flex justify-between text-sm"><span>{manager.manager_name}</span><b>{manager.team_size} employees</b></div><div className="h-2 rounded bg-slate-800"><span className="block h-full rounded bg-blue-500" style={{ width: `${value}%` }} /></div></div> }) : <p className="text-sm text-slate-400">No managers are stored yet.</p>}</div></section>
    </div>
    <div className="mt-4 grid gap-4 xl:grid-cols-3">
      <section className="panel p-5 xl:col-span-2"><h2 className="font-bold">Project Health</h2><div className="mt-4 grid gap-4 md:grid-cols-2">{projects.length ? projects.slice(0, 4).map(project => { const pct = project.status === 'completed' ? 100 : project.status === 'in_progress' ? 55 : 15; return <div className="overflow-hidden rounded-lg border border-slate-800 bg-slate-950/30" key={project.id}>{project.project_image ? <img src={project.project_image} alt={project.name} className="h-24 w-full object-cover" /> : <div className="grid h-24 place-items-center bg-[#131c29] text-blue-400"><Icon name="grid" /></div>}<div className="p-4"><div className="mb-2 flex items-center justify-between gap-3"><div><b>{project.name}</b><p className="text-xs text-blue-200/60">{project.assigned_employee_count || 0} members Â· {project.task_count || 0} tasks</p></div><Badge value={project.active_status || 'active'} /></div><div className="h-2 rounded bg-slate-800"><span className="block h-full rounded bg-emerald-500" style={{ width: `${pct}%` }} /></div></div></div> }) : <p className="text-sm text-slate-400">No projects are stored yet.</p>}</div></section>
      <section className="panel p-5"><h2 className="font-bold">Workload Support</h2><p className="text-sm text-blue-200/70">Employees needing admin attention</p><div className="mt-4 space-y-3"><div className="rounded-md bg-slate-950/40 px-3 py-2"><div className="mb-1 flex justify-between text-sm"><b>Unassigned employees</b><span className="text-blue-200/60">{data.attention.unassigned_employees || 0}</span></div><div className="h-2 rounded bg-slate-800"><span className="block h-full rounded bg-orange-400" style={{ width: `${Math.min(100, ((data.attention.unassigned_employees || 0) / Math.max(totalEmployees, 1)) * 100)}%` }} /></div></div></div></section>
    </div>
    <section className="panel mt-4 overflow-hidden"><div className="flex items-center justify-between px-4 py-3"><div><h2 className="font-bold">Reports</h2><p className="text-sm text-blue-200/70">Work logs and billing summary from the database</p></div><button className="btn-secondary text-xs">Export Report</button></div>{visibleReports.length ? <Table headers={['Employee Name', 'Project Name', 'Billable Hours', 'Role']}>{visibleReports.slice(0, 5).map((row, index) => <tr key={`${row.employee_id || row.employee_name}-${row.project_id || row.project_name}-${index}`}><Cell><b>{row.employee_name}</b></Cell><Cell>{row.project_name}</Cell><Cell className="font-mono">{formatHours(row.hours_logged)}</Cell><Cell><Badge value={row.role} /></Cell></tr>)}</Table> : <p className="border-t border-slate-800 px-5 py-8 text-sm text-slate-400">No work logs are stored yet.</p>}</section>
  </>
}

function Employees() {
  const [items, setItems] = useState([])
  const [role, setRole] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(true)
  const [editing, setEditing] = useState(null)

  const load = () => {
    setBusy(true)
    setError('')
    api(`/employees${role ? `?role=${role}` : ''}`).then(setItems).catch(error => setError(error.message)).finally(() => setBusy(false))
  }
  useEffect(load, [role])

  const remove = async item => {
    if (!confirm(`Delete ${item.name}?`)) return
    try {
      await api(`/employees/${item.id}`, { method: 'DELETE' })
      load()
    } catch (error) {
      alert(error.message)
    }
  }

  return <>
    <PageTitle title="Manage Employees" subtitle="View and manage all users." action={<button onClick={() => setEditing({})} className="btn-primary inline-flex items-center gap-1.5 px-3 py-1.5 text-xs"><Icon name="plus" />Add Employee</button>} />
    <div className="panel mb-5 p-3"><select className="control max-w-28 px-2 py-1 text-xs" value={role} onChange={event => setRole(event.target.value)}><option value="">Role</option><option value="employee">Employee</option><option value="manager">Manager</option><option value="admin">Admin</option></select></div>
    {busy ? <Loading /> : error ? <Empty message={error} /> : <Table headers={['Name', 'Email', 'Role', 'Status', 'Manager', 'Projects', 'Actions']}>{items.map(item => <tr key={item.id}>
      <Cell><b>{item.name}</b></Cell>
      <Cell className="font-mono text-slate-400">{item.email}</Cell>
      <Cell><Badge value={item.role} /></Cell>
      <Cell><Badge value={item.status || 'active'} /></Cell>
      <Cell>{item.manager?.name || '-'}</Cell>
      <Cell>{item.projects.map(project => project.name).join(', ') || '-'}</Cell>
      <Cell><div className="flex gap-3"><button title="Edit employee" className="text-slate-400 hover:text-white" onClick={() => setEditing(item)}><Icon name="edit" /></button><button title="Delete employee" className="text-rose-400 hover:text-rose-300" onClick={() => remove(item)}><Icon name="trash" /></button></div></Cell>
    </tr>)}</Table>}
    {editing && <EmployeeForm employee={editing.id ? editing : null} onClose={() => setEditing(null)} onSaved={() => { setEditing(null); load() }} />}
  </>
}

function Managers() {
  const [managers, setManagers] = useState([])
  const [employees, setEmployees] = useState([])
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('')
  const [editing, setEditing] = useState(null)
  const [assigning, setAssigning] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(true)

  const load = () => {
    setBusy(true)
    setError('')
    Promise.all([api('/employees?role=manager'), api('/employees?role=employee')])
      .then(([managerRows, employeeRows]) => { setManagers(managerRows); setEmployees(employeeRows) })
      .catch(error => setError(error.message))
      .finally(() => setBusy(false))
  }
  useEffect(load, [])

  const remove = async manager => {
    if (!confirm(`Delete manager ${manager.name}?`)) return
    try {
      await api(`/employees/${manager.id}`, { method: 'DELETE' })
      load()
    } catch (error) {
      alert(error.message)
    }
  }
  const assign = async event => {
    event.preventDefault()
    const selected = new FormData(event.target).getAll('employee_ids').map(Number)
    try {
      await Promise.all(employees.map(employee => api(`/employees/${employee.id}/manager`, {
        method: 'PUT',
        body: JSON.stringify({ manager_id: selected.includes(employee.id) ? assigning.id : null }),
      })))
      setAssigning(null)
      load()
    } catch (error) {
      alert(error.message)
    }
  }

  const filtered = managers.filter(manager => (!status || (manager.status || 'active') === status) && `${manager.name} ${manager.email}`.toLowerCase().includes(query.toLowerCase()))
  const cards = [['Total Managers', managers.length, 'user', 'text-blue-400'], ['Active', managers.filter(manager => (manager.status || 'active') === 'active').length, 'chart', 'text-emerald-400'], ['Inactive', managers.filter(manager => manager.status === 'inactive').length, 'chart', 'text-orange-400']]

  return <>
    <PageTitle title="Managers" subtitle="Manage manager records and employee assignments." action={<button onClick={() => setEditing({ role: 'manager' })} className="btn-primary inline-flex items-center gap-1.5 px-3 py-1.5 text-xs"><Icon name="plus" />Add Manager</button>} />
    <div className="mb-5 grid gap-4 md:grid-cols-3">{cards.map(([label, value, icon, color]) => <div className="panel flex items-center gap-4 p-4" key={label}><span className={`grid h-12 w-12 place-items-center rounded-lg bg-white/5 ${color}`}><Icon name={icon} /></span><div><b className="block text-2xl">{value}</b><p className="text-sm text-blue-200/70">{label}</p></div></div>)}</div>
    <div className="panel mb-5 flex flex-wrap gap-3 p-3"><input className="control max-w-sm" placeholder="Search managers..." value={query} onChange={event => setQuery(event.target.value)} /><select className="control max-w-36" value={status} onChange={event => setStatus(event.target.value)}><option value="">All Status</option><option value="active">Active</option><option value="inactive">Inactive</option></select></div>
    {busy ? <Loading /> : error ? <Empty message={error} /> : <Table headers={['Manager Name', 'Email', 'Team Size', 'Projects', 'Status', 'Actions']}>{filtered.map(manager => <tr key={manager.id}><Cell><b>{manager.name}</b></Cell><Cell className="font-mono text-slate-400">{manager.email}</Cell><Cell>{employees.filter(employee => employee.manager?.id === manager.id).length}</Cell><Cell>{manager.projects?.map(project => project.name).join(', ') || '-'}</Cell><Cell><Badge value={manager.status || 'active'} /></Cell><Cell><div className="flex gap-3"><button title="Assign employees" className="text-blue-400 hover:text-blue-300" onClick={() => setAssigning(manager)}><Icon name="user" /></button><button title="Edit manager" className="text-slate-400 hover:text-white" onClick={() => setEditing(manager)}><Icon name="edit" /></button><button title="Delete manager" className="text-rose-400 hover:text-rose-300" onClick={() => remove(manager)}><Icon name="trash" /></button></div></Cell></tr>)}</Table>}
    {editing && <EmployeeForm employee={editing.id ? editing : null} fixedRole="manager" onClose={() => setEditing(null)} onSaved={() => { setEditing(null); load() }} />}
    {assigning && <Modal title={`Assign employees to ${assigning.name}`} onClose={() => setAssigning(null)}><form onSubmit={assign} className="grid gap-3 p-5"><div className="max-h-80 overflow-y-auto rounded border border-slate-800">{employees.map(employee => <label key={employee.id} className="flex items-center justify-between gap-3 border-b border-slate-800 px-3 py-2 text-sm"><span><input type="checkbox" name="employee_ids" value={employee.id} defaultChecked={employee.manager?.id === assigning.id} className="mr-2" />{employee.name}</span><Badge value={employee.status || 'active'} /></label>)}</div><Actions onClose={() => setAssigning(null)} text="Save assignments" /></form></Modal>}
  </>
}

function EmployeeForm({ employee, fixedRole, onClose, onSaved }) {
  const [error, setError] = useState('')
  const [managers, setManagers] = useState([])
  const [projects, setProjects] = useState([])
  const [selectedRole, setSelectedRole] = useState(fixedRole || employee?.role || 'employee')
  useEffect(() => {
    api('/employees?role=manager').then(setManagers).catch(() => {})
    api('/projects').then(setProjects).catch(() => {})
  }, [])
  const submit = async event => {
    event.preventDefault()
    const formData = new FormData(event.target)
    const form = Object.fromEntries(formData)
    const project_ids = formData.getAll('project_ids').map(Number)
    const payload = {
      username: form.username.trim(),
      name: form.name.trim(),
      email: form.email.trim(),
      role: selectedRole,
      status: form.status,
    }
    if (!employee) payload.password = form.password
    if (!employee && selectedRole === 'employee') {
      payload.project_ids = project_ids
    }
    try {
      const saved = await api(employee ? `/employees/${employee.id}` : '/employees', { method: employee ? 'PUT' : 'POST', body: JSON.stringify(payload) })
      const id = employee?.id || saved.id
      if (employee && selectedRole === 'employee') {
        await api(`/employees/${id}/manager`, { method: 'PUT', body: JSON.stringify({ manager_id: form.manager_id ? Number(form.manager_id) : null }) })
        await api(`/employees/${id}/projects`, { method: 'PUT', body: JSON.stringify({ project_ids }) })
      }
      onSaved()
    } catch (error) {
      setError(error.message)
    }
  }
  return <Modal title={employee ? 'Edit employee' : 'Add employee'} onClose={onClose}><form onSubmit={submit} className="grid gap-4 p-5">
    <div className="grid gap-4 sm:grid-cols-2"><Field label="Name" name="name" defaultValue={employee?.name || ''} required /><Field label="Username" name="username" defaultValue={employee?.username || ''} required /></div>
    <Field label="Email" name="email" type="email" defaultValue={employee?.email || ''} required />
    <div className="grid gap-4 sm:grid-cols-2">{fixedRole ? <input type="hidden" name="role" value={fixedRole} /> : <Select label="Role" name="role" value={selectedRole} onChange={event => setSelectedRole(event.target.value)} options={['employee', 'manager', 'admin']} />}<Select label="Status" name="status" defaultValue={employee?.status || 'active'} options={['active', 'inactive']} /></div>
    {selectedRole === 'employee' && <div className="grid gap-4 sm:grid-cols-2">{employee && <label><span className="label">Manager</span><select name="manager_id" className="control" defaultValue={employee?.manager?.id || ''}><option value="">No manager</option>{managers.map(manager => <option key={manager.id} value={manager.id}>{manager.name}</option>)}</select></label>}<label><span className="label">Projects</span><select name="project_ids" multiple className="control min-h-28" defaultValue={employee?.projects?.map(project => String(project.id)) || []}>{projects.map(project => <option key={project.id} value={project.id}>{project.name}</option>)}</select></label></div>}
    {!employee && <Field label="Password" name="password" type="password" minLength="8" required />}
    <FormError error={error} /><Actions onClose={onClose} text={employee ? 'Save employee' : 'Add employee'} />
  </form></Modal>
}

function Projects() {
  const [items, setItems] = useState([])
  const [status, setStatus] = useState('')
  const [show, setShow] = useState(false)
  const [editing, setEditing] = useState(null)
  const [tasks, setTasks] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(true)
  const [sort, setSort] = useState('duration_desc')

  const load = () => {
    setBusy(true)
    setError('')
    api(`/projects${status ? `?status=${status}` : ''}`).then(setItems).catch(error => setError(error.message)).finally(() => setBusy(false))
  }
  useEffect(load, [status])

  const remove = async project => {
    if (!confirm(`Delete ${project.name}? Projects with tasks cannot be deleted.`)) return
    try {
      await api(`/projects/${project.id}`, { method: 'DELETE' })
      load()
    } catch (error) {
      alert(error.message)
    }
  }
  const openTasks = async project => {
    try {
      setTasks({ project, items: await api(`/projects/${project.id}/tasks`) })
    } catch (error) {
      alert(error.message)
    }
  }

  return <>
    <PageTitle title="Projects & Tasks" subtitle="Manage projects and their tasks." action={<button className="btn-primary inline-flex items-center gap-1.5 px-3 py-1.5 text-xs" onClick={() => setShow(true)}><Icon name="plus" />Add Project</button>} />
    <div className="panel mb-5 flex items-center justify-between gap-4 p-3"><select className="control max-w-32 px-2 py-1 text-xs" value={status} onChange={event => setStatus(event.target.value)}><option value="">Progress</option><option value="created">Created</option><option value="in_progress">In progress</option><option value="completed">Completed</option></select><div className="flex items-center gap-2 text-xs text-blue-200"><b className="uppercase tracking-widest">Sort</b><select className="control w-36 px-2 py-1 text-xs" value={sort} onChange={event => setSort(event.target.value)}><option value="duration_desc">Duration â†“</option><option value="duration_asc">Duration â†‘</option><option value="hours_desc">Hours â†“</option><option value="hours_asc">Hours â†‘</option></select></div></div>
    {busy ? <Loading /> : error ? <Empty message={error} /> : <Table headers={['Project', 'Manager', 'Tasks', 'Start Date', 'End Date', 'Hours', 'Progress', 'Status', 'Actions']}>{[...items].sort((a, b) => sort === 'hours_asc' ? a.hours_logged - b.hours_logged : sort === 'hours_desc' ? b.hours_logged - a.hours_logged : sort === 'duration_asc' ? new Date(a.end_date) - new Date(b.end_date) : new Date(b.end_date) - new Date(a.end_date)).map(project => <tr key={project.id}>
      <Cell><div className="flex items-center gap-3">{project.project_image ? <img src={project.project_image} alt={project.name} className="h-12 w-12 rounded-md object-cover" /> : <span className="grid h-12 w-12 place-items-center rounded-md bg-slate-800 text-blue-400"><Icon name="grid" /></span>}<b>{project.name}</b></div></Cell>
      <Cell>{project.manager?.name || '-'}</Cell>
      <Cell><button onClick={() => openTasks(project)} className="text-blue-400 hover:text-blue-300">{project.task_count} tasks</button></Cell>
      <Cell className="font-mono">{project.start_date}</Cell>
      <Cell className="font-mono">{project.end_date}</Cell>
      <Cell className="font-mono text-cyan-400">{formatHours(project.hours_logged)}</Cell>
      <Cell><Badge value={project.status} /></Cell>
      <Cell><Badge value={project.active_status || 'active'} /></Cell>
      <Cell><div className="flex gap-3"><button title="Edit project" className="text-slate-400 hover:text-white" onClick={() => setEditing(project)}><Icon name="edit" /></button><button title="Delete project" className="text-rose-400 hover:text-rose-300" onClick={() => remove(project)}><Icon name="trash" /></button></div></Cell>
    </tr>)}</Table>}
    {show && <ProjectForm onClose={() => setShow(false)} onSaved={() => { setShow(false); load() }} />}
    {editing && <ProjectForm project={editing} onClose={() => setEditing(null)} onSaved={() => { setEditing(null); load() }} />}
    {tasks && <TaskModal data={tasks} onClose={() => setTasks(null)} onReload={openTasks} />}
  </>
}

function ProjectForm({ project, onClose, onSaved }) {
  const [error, setError] = useState('')
  const [managers, setManagers] = useState([])
  const [imagePreview, setImagePreview] = useState(project?.project_image || '')
  useEffect(() => { api('/employees?role=manager').then(setManagers).catch(() => {}) }, [])
  const submit = async event => {
    event.preventDefault()
    const formData = new FormData(event.target)
    const form = Object.fromEntries(formData)
    const manager_id = form.manager_id ? Number(form.manager_id) : null
    const image = await readImage(formData.get('project_image'))
    const payload = { ...form, project_image: image || imagePreview || null }
    delete payload.manager_id
    if (!project) payload.manager_id = manager_id
    try {
      await api(project ? `/projects/${project.id}` : '/projects', { method: project ? 'PUT' : 'POST', body: JSON.stringify(payload) })
      if (project) await api(`/projects/${project.id}/manager`, { method: 'PUT', body: JSON.stringify({ manager_id }) })
      onSaved()
    } catch (error) {
      setError(error.message)
    }
  }
  return <Modal title={project ? 'Edit project' : 'Add project'} onClose={onClose}><form onSubmit={submit} className="grid gap-3 p-5">
    <Field label="Project name" name="name" defaultValue={project?.name || ''} required />
    <label><span className="label">Project photo</span><input name="project_image" type="file" accept="image/*" className="control" onChange={async event => setImagePreview(await readImage(event.target.files?.[0]) || project?.project_image || '')} required={!project} /></label>
    {imagePreview && <img src={imagePreview} alt="Project preview" className="h-32 w-full rounded-md border border-slate-800 object-cover" />}
    <label><span className="label">Description</span><textarea name="description" className="control min-h-16" defaultValue={project?.description || ''} /></label>
    <div className="grid gap-3 sm:grid-cols-2"><Field label="Start date" name="start_date" type="date" defaultValue={project?.start_date || ''} required /><Field label="End date" name="end_date" type="date" defaultValue={project?.end_date || ''} required /></div>
    <div className="grid gap-3 sm:grid-cols-2"><Select label="Progress" name="status" defaultValue={project?.status || 'created'} options={['created', 'in_progress', 'completed']} /><Select label="Status" name="active_status" defaultValue={project?.active_status || 'active'} options={['active', 'inactive']} /></div>
    <label><span className="label">Manager</span><select name="manager_id" className="control" defaultValue={project?.manager?.id || ''}><option value="">No manager</option>{managers.map(manager => <option key={manager.id} value={manager.id}>{manager.name}</option>)}</select></label>
    <FormError error={error} /><Actions onClose={onClose} text={project ? 'Save project' : 'Create project'} />
  </form></Modal>
}

function TaskModal({ data, onClose, onReload }) {
  const [error, setError] = useState('')
  const add = async event => {
    event.preventDefault()
    try {
      await api(`/projects/${data.project.id}/tasks`, { method: 'POST', body: JSON.stringify(Object.fromEntries(new FormData(event.target))) })
      event.target.reset()
      onReload(data.project)
    } catch (error) {
      setError(error.message)
    }
  }
  return <Modal title={`${data.project.name} tasks`} onClose={onClose}>
    <div className="max-h-56 overflow-y-auto">{data.items.length ? data.items.map(task => <div className="border-b border-slate-800 px-5 py-3" key={task.id}><b>{task.name}</b><p className="text-sm text-slate-400">{task.description || 'No description'}</p></div>) : <p className="p-5 text-slate-400">No tasks yet.</p>}</div>
    <form onSubmit={add} className="grid gap-3 p-5"><Field label="New task" name="name" required /><Field label="Description" name="description" /><FormError error={error} /><Actions onClose={onClose} text="Add task" /></form>
  </Modal>
}

function Reports() {
  const [projects, setProjects] = useState([])
  const [rows, setRows] = useState([])
  const [filters, setFilters] = useState({})
  const [error, setError] = useState('')
  useEffect(() => { api('/projects').then(setProjects).catch(error => setError(error.message)) }, [])
  const load = () => {
    const params = new URLSearchParams(Object.entries(filters).filter(([, value]) => value))
    api(`/reports?${params}`).then(setRows).catch(error => setError(error.message))
  }
  useEffect(load, [])
  const change = event => setFilters({ ...filters, [event.target.name]: event.target.value })
  return <><PageTitle title="Reports" subtitle="Hours breakdown by employee and project." /><div className="panel mb-5 grid gap-3 p-4 md:grid-cols-5"><select name="project_id" onChange={change} className="control"><option value="">Projects</option>{projects.map(project => <option value={project.id} key={project.id}>{project.name}</option>)}</select><Select name="type" onChange={change} options={['', 'standard', 'over_time']} placeholder="Type" /><Select name="role" onChange={change} options={['', 'employee', 'manager']} placeholder="Role" /><input name="start_date" onChange={change} className="control" type="date" /><button className="btn-primary" onClick={load}>Apply</button></div>{error ? <Empty message={error} /> : <Table headers={['Employee', 'Role', 'Project', 'Hours Logged']}>{rows.map((row, index) => <tr key={`${row.employee_id}-${row.project_id}-${index}`}><Cell><b>{row.employee_name}</b></Cell><Cell><Badge value={row.role} /></Cell><Cell>{row.project_name}</Cell><Cell className="font-mono text-cyan-400">{formatHours(row.hours_logged)}</Cell></tr>)}</Table>}</>
}

const isoToday = () => new Date().toISOString().slice(0, 10)
const timeDiffHours = (start, end) => start && end ? Math.max(0, (new Date(`2000-01-01T${end}`) - new Date(`2000-01-01T${start}`)) / 3600000) : 0

function EmployeeTimesheet({ isManager }) {
  const [context, setContext] = useState(null)
  const [rows, setRows] = useState([{ project_id: '', task_id: '', work_date: isoToday(), start_time: '09:00', end_time: '13:00', type: 'standard', comments: '' }])
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [taskEditor, setTaskEditor] = useState(null)
  const [busyTaskAction, setBusyTaskAction] = useState(false)

  useEffect(() => { api(`/${isManager ? 'manager' : 'employee'}/context`).then(setContext).catch(error => setError(error.message)) }, [isManager])
  if (error) return <><PageTitle title="New Timesheet" subtitle="Log your work for today." /><Empty message={error} /></>
  if (!context) return <Loading />

  const update = (index, patch) => setRows(items => items.map((row, rowIndex) => rowIndex === index ? { ...row, ...patch } : row))
  const addRow = () => setRows(items => [...items, { project_id: '', task_id: '', work_date: isoToday(), start_time: '', end_time: '', type: 'standard', comments: '' }])
  const closeTaskEditor = () => setTaskEditor(null)
  const openTaskEditor = (mode, projectId, rowIndex, task) => setTaskEditor({ mode, projectId, rowIndex, task, name: task?.name || '', description: task?.description || '' })

  const refreshProjectTasks = (projectId, callback) => {
    api(`/projects/${projectId}/tasks`).then(tasks => {
      setContext(current => {
        if (!current) return current
        return {
          ...current,
          projects: current.projects.map(project => project.id === projectId ? { ...project, tasks } : project),
        }
      })
      if (callback) callback(tasks)
    }).catch(error => setError(error.message))
  }

  const saveTask = async () => {
    if (!taskEditor || !taskEditor.projectId) return
    if (!taskEditor.name.trim()) return setError('Task name is required.')
    setError('')
    setBusyTaskAction(true)
    try {
      let savedTask
      if (taskEditor.mode === 'create') {
        savedTask = await api(`/projects/${taskEditor.projectId}/tasks`, {
          method: 'POST',
          body: JSON.stringify({ name: taskEditor.name.trim(), description: taskEditor.description.trim() || null }),
        })
      } else {
        savedTask = await api(`/tasks/${taskEditor.task.id}`, {
          method: 'PUT',
          body: JSON.stringify({ name: taskEditor.name.trim(), description: taskEditor.description.trim() || null }),
        })
      }
      refreshProjectTasks(taskEditor.projectId, tasks => {
        if (taskEditor.mode === 'create') {
          update(taskEditor.rowIndex, { task_id: String(savedTask.id) })
        }
      })
      closeTaskEditor()
    } catch (error) {
      setError(error.message)
    } finally {
      setBusyTaskAction(false)
    }
  }

  const deleteTask = async (task, projectId) => {
    if (!confirm(`Delete task ${task.name}?`)) return
    try {
      await api(`/tasks/${task.id}`, { method: 'DELETE' })
      setContext(current => {
        if (!current) return current
        return {
          ...current,
          projects: current.projects.map(project => project.id === projectId ? { ...project, tasks: (project.tasks || []).filter(item => item.id !== task.id) } : project),
        }
      })
      setRows(items => items.map(row => (String(row.task_id) === String(task.id) ? { ...row, task_id: '' } : row)))
    } catch (error) {
      setError(error.message)
    }
  }

  const submit = async () => {
    setError('')
    setMessage('')
    const entries = rows.filter(row => row.task_id && row.start_time && row.end_time).map(row => ({ task_id: Number(row.task_id), work_date: row.work_date, start_time: row.start_time, end_time: row.end_time, type: row.type, comments: row.comments || null }))
    if (!entries.length) return setError('Add at least one complete timesheet row.')
    try {
      const endpoint = isManager ? '/manager/timesheets' : '/employee/timesheets'
    const result = await api(endpoint, { method: 'POST', body: JSON.stringify({ user_id: context.employee.id, entries }) })
      setMessage(`${result.created} timesheet row${result.created === 1 ? '' : 's'} submitted.`)
      setRows([{ project_id: '', task_id: '', work_date: isoToday(), start_time: '09:00', end_time: '13:00', type: 'standard', comments: '' }])
    } catch (error) {
      setError(error.message)
    }
  }

  return <><PageTitle title="New Timesheet" subtitle="Log your work for today. All rows are submitted together." action={<button className="btn-primary" onClick={submit}>Submit Timesheet</button>} />
    <section className="panel overflow-hidden"><div className="grid min-w-[1050px] grid-cols-[1.2fr_1.2fr_.9fr_.8fr_.8fr_.9fr_1.7fr_0.7fr] gap-3 bg-[#131c29] px-4 py-3 text-sm font-bold uppercase tracking-widest text-slate-400"><span>Project</span><span>Task</span><span>Date</span><span>Start</span><span>End</span><span>Type</span><span>Comments</span><span>Action</span></div>
      <div className="overflow-x-auto">{rows.map((row, index) => {
        const project = context.projects.find(item => String(item.id) === String(row.project_id))
        const task = project?.tasks?.find(task => String(task.id) === String(row.task_id))
        return <div className="grid min-w-[1050px] grid-cols-[1.2fr_1.2fr_.9fr_.8fr_.8fr_.9fr_1.7fr_0.7fr] gap-3 border-t border-slate-800 px-4 py-3" key={index}>
          <select className="control" value={row.project_id} onChange={event => update(index, { project_id: event.target.value, task_id: '' })}>
            <option value="">Project</option>
            {context.projects.map(project => <option key={project.id} value={project.id}>{project.name}</option>)}
          </select>
          <div className="flex items-center gap-2">
            <select className="control flex-1" value={row.task_id} onChange={event => {
              const value = event.target.value
              if (value === '__create__') {
                openTaskEditor('create', Number(row.project_id), index, null)
              } else {
                update(index, { task_id: value })
              }
            }}>
              <option value="">Task</option>
              {project?.tasks?.map(task => <option key={task.id} value={task.id}>{task.name}</option>)}
              {project ? <option value="__create__">+ Create new task...</option> : null}
            </select>
          </div>
          <input className="control" type="date" value={row.work_date} onChange={event => update(index, { work_date: event.target.value })} />
          <input className="control" type="time" value={row.start_time} onChange={event => update(index, { start_time: event.target.value })} />
          <input className="control" type="time" value={row.end_time} onChange={event => update(index, { end_time: event.target.value })} />
          <select className="control" value={row.type} onChange={event => update(index, { type: event.target.value })}>
            <option value="standard">Standard</option>
            <option value="over_time">Over time</option>
          </select>
          <input className="control" placeholder="Optional notes..." value={row.comments} onChange={event => update(index, { comments: event.target.value })} />
          <div className="flex items-center justify-start gap-2">
            <button
              type="button"
              className="btn-secondary text-xs px-2 py-1"
              onClick={() => {
                if (!row.project_id) {
                  setError('Please select a project before editing this row.')
                  return
                }
                openTaskEditor(task ? 'edit' : 'create', Number(row.project_id), index, task)
              }}
            >Edit</button>
            <button
              type="button"
              className="btn-secondary text-xs px-2 py-1 text-rose-300"
              onClick={() => {
                if (task) {
                  deleteTask(task, project?.id)
                } else {
                  setRows(items => items.filter((_, rowIndex) => rowIndex !== index))
                }
              }}
            >Delete</button>
          </div>
        </div>
      })}</div>
      <button className="m-4 text-sm font-bold text-blue-300 hover:text-blue-200" onClick={addRow} type="button">+ Add row</button>
    </section>
    {taskEditor && <Modal title={taskEditor.mode === 'create' ? 'Create task' : 'Edit task'} onClose={closeTaskEditor}>
      <form onSubmit={event => { event.preventDefault(); saveTask() }} className="grid gap-4 p-5">
        <Field label="Task name" name="task_name" value={taskEditor.name} onChange={event => setTaskEditor(current => ({ ...current, name: event.target.value }))} required />
        <label><span className="label">Description</span><textarea className="control min-h-24" value={taskEditor.description} onChange={event => setTaskEditor(current => ({ ...current, description: event.target.value }))} /></label>
        <FormError error={error} />
        <div className="flex items-center justify-between gap-3">
          {taskEditor.mode === 'edit' ? <button type="button" className="btn-secondary text-rose-300" onClick={() => deleteTask(taskEditor.task, taskEditor.projectId)}>Delete task</button> : <span />}
          <div className="flex gap-3">
            <button type="button" className="btn-secondary" onClick={closeTaskEditor}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={busyTaskAction}>{taskEditor.mode === 'create' ? 'Create task' : 'Save task'}</button>
          </div>
        </div>
      </form>
    </Modal>}
    <div className="mt-4 flex gap-4 text-sm">{message && <p className="text-emerald-400">{message}</p>}{error && <p className="text-rose-400">{error}</p>}<p className="ml-auto text-blue-200/70">Total: {formatHours(rows.reduce((total, row) => total + timeDiffHours(row.start_time, row.end_time), 0))}</p></div></>
}

function EmployeeHistory({ isManager }) {
  const [context, setContext] = useState(null)
  const [rows, setRows] = useState([])
  const [filters, setFilters] = useState({})
  const [error, setError] = useState('')

  useEffect(() => { api(`/${isManager ? 'manager' : 'employee'}/context`).then(data => { setContext(data); return api(`/history/${data.employee.id}`) }).then(setRows).catch(error => setError(error.message)) }, [isManager])
  const load = () => {
    if (!context) return
    const params = new URLSearchParams(Object.entries(filters).filter(([, value]) => value))
    api(`/history/${context.employee.id}?${params}`).then(setRows).catch(error => setError(error.message))
  }
  const change = event => setFilters({ ...filters, [event.target.name]: event.target.value })
  const total = rows.reduce((sum, row) => sum + Number(row.duration_hours || 0), 0)

  if (error) return <><PageTitle title="Work History" subtitle="Submitted work logs." /><Empty message={error} /></>
  if (!context) return <Loading />
  return <><PageTitle title="Work History" subtitle="Submitted work logs." /><div className="panel mb-5 grid gap-3 p-4 md:grid-cols-5"><select name="project_id" onChange={change} className="control"><option value="">Projects</option>{context.projects.map(project => <option value={project.id} key={project.id}>{project.name}</option>)}</select><Select name="type" onChange={change} options={['', 'standard', 'over_time']} placeholder="Type" /><input name="start_date" onChange={change} className="control" type="date" /><input name="end_date" onChange={change} className="control" type="date" /><button className="btn-primary" onClick={load}>Apply</button></div>{rows.length ? <><Table headers={['Project', 'Task', 'Date', 'Start', 'Duration', 'Type', 'Comments']}>{rows.map(row => <tr key={row.work_id}><Cell><b>{row.project_name}</b></Cell><Cell>{row.task_name}</Cell><Cell className="font-mono">{String(row.start_time).slice(0, 10)}</Cell><Cell className="font-mono">{String(row.start_time).slice(11, 16)}</Cell><Cell className="font-mono text-cyan-400">{formatHours(row.duration_hours)}</Cell><Cell><Badge value={row.type} /></Cell><Cell>{row.comments || '-'}</Cell></tr>)}</Table><p className="mt-3 text-right font-mono text-cyan-400">Total: {formatHours(total)}</p></> : <Empty message="No work history yet." />}</>
}

function ManagerDashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [range, setRange] = useState({ start: '2026-06-20', end: '2026-06-24' })
  const [appliedRange, setAppliedRange] = useState({ start: '2026-06-20', end: '2026-06-24' })

  useEffect(() => {
    api('/dashboard')
      .then(setData)
      .catch(error => setError(error.message))
  }, [])

  const applyRange = () => setAppliedRange(range)

  if (error) return <><PageTitle title="Manager Dashboard" subtitle="Overview of your team and projects." /><Empty message={error} /></>
  if (!data) return <Loading />

  const projects = data.projects
  const managers = data.team_workload
  const totalProjects = data.statistics.total_projects || 0
  const totalManagers = data.statistics.total_managers || 0
  const totalEmployees = data.statistics.total_employees || 0
  const completed = projects.filter(project => project.status === 'completed').length
  const inProgress = projects.filter(project => project.status === 'in_progress').length
  const inactive = projects.filter(project => project.active_status === 'inactive').length
  const progress = Math.round((completed / Math.max(projects.length, 1)) * 100)
  const rangeLabel = `${new Date(appliedRange.start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${new Date(appliedRange.end).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`

  return <>
    <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div><h1 className="text-3xl font-black tracking-tight">Manager Dashboard</h1><p className="text-blue-200/80">Overview of your team, assignments, and project analytics · {rangeLabel}</p></div>
      <div className="flex flex-wrap items-center gap-2 rounded-lg border border-slate-700 bg-[#101620] px-3 py-2 text-sm text-blue-100"><span className="text-blue-400"><Icon name="chart" /></span><input aria-label="Start date" type="date" className="control w-36 px-2 py-1 text-xs" value={range.start} onChange={event => setRange({ ...range, start: event.target.value })} /><span className="text-slate-500">to</span><input aria-label="End date" type="date" className="control w-36 px-2 py-1 text-xs" value={range.end} onChange={event => setRange({ ...range, end: event.target.value })} /><button className="btn-primary px-3 py-1.5 text-xs" onClick={applyRange}>Apply</button></div>
    </div>
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">{[
      ['Projects', totalProjects, `${projects.filter(project => project.active_status !== 'inactive').length} Active`, 'grid', 'text-violet-400', 'bg-violet-500'],
      ['Managers', totalManagers, `${managers.reduce((total, manager) => total + Number(manager.team_size || 0), 0)} Employees`, 'user', 'text-blue-400', 'bg-blue-500'],
      ['Employees', totalEmployees, `${data.attention.unassigned_employees || 0} Unassigned`, 'user', 'text-emerald-400', 'bg-emerald-500'],
      ['Completed', completed, `${projects.length - completed} Open`, 'chart', 'text-emerald-400', 'bg-emerald-500'],
      ['Progress', `${progress}%`, 'Project completion', 'chart', 'text-rose-400', 'bg-rose-500'],
    ].map(([label, value, text, icon, color, bg]) => <div className="panel p-4" key={label}><div className="flex items-center gap-4"><span className={`grid h-12 w-12 place-items-center rounded-lg bg-white/5 ${bg}`}><Icon name={icon} /></span><div><b className="block text-2xl text-white">{value}</b><p className="text-sm font-semibold text-slate-300">{label}</p><small className="text-blue-200/70">{text}</small></div></div></div>)} </div>
    <div className="mt-4 grid gap-4 xl:grid-cols-12">
      <section className="panel p-5 xl:col-span-4"><h2 className="font-bold">Team Workload</h2><div className="mt-5 space-y-3">{managers.slice(0, 4).map(manager => <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4" key={manager.manager_id}><div className="flex items-center justify-between gap-3"><div><b>{manager.manager_name}</b><p className="text-sm text-blue-200/70">{manager.team_size} team members</p></div><span className="rounded-full bg-blue-950 px-3 py-1 text-xs uppercase text-blue-300">{formatHours(manager.hours_logged)}</span></div></div>)}</div></section>
      <section className="panel p-5 xl:col-span-5"><h2 className="font-bold">Project Overview</h2><div className="mt-5 grid gap-4">{projects.slice(0, 4).map(project => <div key={project.id} className="overflow-hidden rounded-lg border border-slate-800 bg-slate-950/40"><div className="p-4"><div className="flex items-center justify-between gap-3"><div><b>{project.name}</b><p className="text-sm text-blue-200/70">{project.assigned_employee_count} employees · {project.task_count} tasks</p></div><Badge value={project.active_status} /></div><div className="mt-3 h-2 rounded bg-slate-800"><span className="block h-full rounded bg-emerald-500" style={{ width: `${project.status === 'completed' ? 100 : project.status === 'in_progress' ? 60 : 20}%` }} /></div></div></div>)} </div></section>
      <section className="panel p-5 xl:col-span-3"><h2 className="font-bold">Attention</h2><div className="mt-5 space-y-4"><div className="rounded-lg bg-slate-950/40 p-4"><div className="flex items-center justify-between text-sm"><span>Unassigned employees</span><strong>{data.attention.unassigned_employees}</strong></div><div className="mt-3 h-2 rounded bg-slate-800"><span className="block h-full rounded bg-orange-400" style={{ width: `${Math.min(100, ((data.attention.unassigned_employees || 0) / Math.max(totalEmployees, 1)) * 100)}%` }} /></div></div><div className="rounded-lg bg-slate-950/40 p-4"><div className="flex items-center justify-between text-sm"><span>Due within 7 days</span><strong>{data.attention.projects_due_within_seven_days}</strong></div></div></div></section>
    </div>
  </>
}

function Profile() {
  const [profile, setProfile] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => { api('/employees?role=admin').then(items => items[0] ? api(`/profile/${items[0].id}`) : Promise.reject(new Error('No admin user exists yet.'))).then(setProfile).catch(error => setError(error.message)) }, [])
  if (error) return <><PageTitle title="My Profile" subtitle="Account information." /><Empty message={error} /></>
  if (!profile) return <Loading />
  return <><PageTitle title="My Profile" subtitle="Account information." /><section className="panel max-w-xl overflow-hidden"><div className="flex items-center gap-4 bg-[#131b27] p-6"><span className="grid h-14 w-14 place-items-center rounded-full border border-blue-700 bg-blue-950 text-2xl text-blue-400">{profile.name.split(' ').map(word => word[0]).join('').slice(0, 2)}</span><div><h2 className="text-xl font-bold">{profile.name}</h2><Badge value={profile.role} /></div></div>{[['User ID', profile.username], ['Email', profile.email], ['Role', profile.role], ['Password', '********']].map(([label, value]) => <div className="flex justify-between border-t border-slate-800 px-6 py-4" key={label}><b className="text-sm uppercase tracking-wide text-blue-200">{label}</b><span className="font-mono">{value}</span></div>)}</section></>
}

function Modal({ title, children, onClose }) {
  return <div className="fixed inset-0 z-30 grid place-items-center bg-black/70 p-4"><section className="w-full max-w-lg rounded-lg border border-slate-700 bg-[#121a27] shadow-2xl"><header className="flex items-center justify-between border-b border-slate-700 px-5 py-4"><h2 className="font-semibold">{title}</h2><button onClick={onClose} className="text-slate-400 hover:text-white"><Icon name="close" /></button></header>{children}</section></div>
}

const PageTitle = ({ title, subtitle, action }) => <div className="mb-6 flex flex-wrap items-end justify-between gap-4"><div><h1 className="text-2xl font-bold tracking-tight">{title}</h1><p className="mt-1 text-lg text-blue-200/80">{subtitle}</p></div>{action}</div>
const Loading = () => <div className="panel p-10 text-center text-slate-400">Loading data...</div>
const Empty = ({ message }) => <div className="panel p-10 text-center text-rose-300">{message}</div>
const Cell = ({ children, className = '' }) => <td className={`border-t border-slate-800 px-4 py-4 text-lg text-slate-300 ${className}`}>{children}</td>
const Table = ({ headers, children }) => <div className="panel overflow-x-auto"><table className="w-full min-w-[900px] border-collapse"><thead className="bg-[#131c29] text-left text-sm uppercase tracking-widest text-slate-400"><tr>{headers.map((header, index) => <th className="px-4 py-3" key={index}>{header}</th>)}</tr></thead><tbody>{children}</tbody></table></div>
const Field = ({ label, ...props }) => <label><span className="label">{label}</span><input className="control" {...props} /></label>
const Select = ({ label, name, options, placeholder, onChange, defaultValue, value }) => <label><span className={label ? 'label' : 'sr-only'}>{label || placeholder}</span><select className="control capitalize" name={name} onChange={onChange} value={value} defaultValue={value === undefined ? defaultValue : undefined}>{placeholder && <option value="">{placeholder}</option>}{options.map(option => <option value={option} key={option}>{option ? option.replace('_', ' ') : 'All'}</option>)}</select></label>
const FormError = ({ error }) => error ? <p className="text-sm text-rose-400">{error}</p> : null
const Actions = ({ onClose, text }) => <div className="flex justify-end gap-3"><button type="button" className="btn-secondary" onClick={onClose}>Cancel</button><button className="btn-primary">{text}</button></div>

export default function App() {
  const [role, setRole] = useState('Admin')
  const [page, setPage] = useState('dashboard')
  const body = useMemo(
    () => ({
      dashboard: <Dashboard />,
      employees: <Employees />,
      managers: <Managers />,
      projects: <Projects />,
      reports: <Reports />,
      profile: <Profile />,
      'employee-timesheet': <EmployeeTimesheet />,
      'employee-history': <EmployeeHistory />,
      'manager-dashboard': <ManagerDashboard />,
      'manager-timesheet': <EmployeeTimesheet isManager />,
      'manager-history': <EmployeeHistory isManager />,
      'team-assignment': <Managers teamMode />,
    })[page],
    [page]
  )
  return <div className="flex min-h-screen"><Sidebar page={page} setPage={setPage} role={role} setRole={setRole} /><main className="min-w-0 flex-1"><Header page={page} role={role} /><div className="mx-auto max-w-7xl p-5 md:p-8">{body}</div></main></div>
}


