from sqlalchemy.orm import Session

from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.ProjectModel import Project
from app.models.RoleModel import Role, RoleEnum
from app.models.UserModel import User
import app.schemas.ProjectSchema as ProjectSchema


class ProjectRepository:

	@staticmethod
	def get_all_projects(current_user: dict, db: Session):
		manager_id = (
			db.query(ProjectAssignment.user_id)
			.join(User, User.id == ProjectAssignment.user_id)
			.join(Role, Role.id == User.role_id)
			.filter(
				ProjectAssignment.project_id == Project.id,
				Role.role == RoleEnum.MANAGER,
			)
			.order_by(ProjectAssignment.user_id)
			.limit(1)
			.correlate(Project)
			.scalar_subquery()
		)
		query = db.query(Project, manager_id.label("manager_id"))

		if current_user["user_role"] != "admin":
			query = query.join(
				ProjectAssignment,
				ProjectAssignment.project_id == Project.id,
			).filter(ProjectAssignment.user_id == current_user["user_id"])

		return query.all()

	@staticmethod
	def get_project_by_id(project_id: int, db: Session):
		return db.query(Project).filter(Project.id == project_id).first()

	@staticmethod
	def is_user_assigned(project_id: int, user_id: int, db: Session):
		return db.query(ProjectAssignment).filter(
			ProjectAssignment.project_id == project_id,
			ProjectAssignment.user_id == user_id,
		).first() is not None

	@staticmethod
	def create_project(data: ProjectSchema.CreateProject, db: Session):
		project = Project(**data.model_dump())
		db.add(project)
		db.commit()
		db.refresh(project)
		return project

	@staticmethod
	def delete_project(project_id: int, db: Session):
		project = ProjectRepository.get_project_by_id(project_id, db)
		if project is None:
			return None

		db.delete(project)
		db.commit()
		return project

	@staticmethod
	def edit_project(
		project_id: int,
		data: ProjectSchema.EditProject,
		db: Session,
	):
		project = ProjectRepository.get_project_by_id(project_id, db)
		if project is None:
			return None

		for key, value in data.model_dump(exclude_unset=True).items():
			if key != "manager_id" and value is not None:
				setattr(project, key, value)

		db.commit()
		db.refresh(project)
		return project
