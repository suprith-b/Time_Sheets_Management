from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.ProjectSchema as ProjectSchema
import app.schemas.ProjectAssignmentSchema as ProjectAssignmentSchema
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.UserRepository import UserRepository
from app.services.UserService import UserService


class ProjectService:

	@staticmethod
	def get_projects(current_user: dict, db: Session):
		projects = ProjectRepository.get_all_projects(current_user, db)
		return [
			ProjectSchema.ProjectResponse.model_validate(project)
			.model_copy(update={"manager_id": manager_id})
			for project, manager_id in projects
		]

	@staticmethod
	def create_project(data: ProjectSchema.CreateProject, db: Session):
		project = ProjectRepository.create_project(data, db)
		return ProjectSchema.ProjectResponse.model_validate(project)

	@staticmethod
	def delete_project(project_id: int, db: Session):
		project = ProjectRepository.delete_project(project_id, db)
		if project is None:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Project not found",
			)
		return ProjectSchema.ProjectResponse.model_validate(project)

	@staticmethod
	def edit_project(
		project_id: int,
		data: ProjectSchema.EditProject,
		current_user: dict,
		db: Session,
	):
		if current_user["user_role"] == "manager":
			changed_fields = set(data.model_dump(exclude_unset=True))
			if not changed_fields.issubset({"end_date", "status"}):
				raise HTTPException(
					status_code=status.HTTP_403_FORBIDDEN,
					detail="Managers can only change end_date and status",
				)
			if not ProjectRepository.is_user_assigned(
				project_id,
				current_user["user_id"],
				db,
			):
				raise HTTPException(
					status_code=status.HTTP_403_FORBIDDEN,
					detail="You do not have permission to edit this project",
				)

		manager_id_changed = "manager_id" in data.model_fields_set
		old_manager_id = None
		if manager_id_changed:
			all_projects = ProjectRepository.get_all_projects(
				{"user_id": current_user["user_id"], "user_role": "admin"},
				db,
			)
			old_manager_id = next(
				(
					manager_id
					for project, manager_id in all_projects
					if project.id == project_id
				),
				None,
			)

			if data.manager_id is not None:
				new_manager = UserRepository.get_user_by_id(
					data.manager_id,
					{"user_id": current_user["user_id"], "user_role": "admin"},
					db,
				)
				if new_manager is None or new_manager.role_id != 2:
					raise HTTPException(
						status_code=status.HTTP_404_NOT_FOUND,
						detail="Manager not found",
					)

		project = ProjectRepository.edit_project(project_id, data, db)
		if project is None:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Project not found",
			)

		if manager_id_changed:
			admin_context = {
				"user_id": current_user["user_id"],
				"user_role": "admin",
			}

			if old_manager_id is not None and old_manager_id != data.manager_id:
				old_manager_projects = ProjectRepository.get_all_projects(
					{"user_id": old_manager_id, "user_role": "manager"},
					db,
				)
				updated_old_project_ids = [
					old_project.id
					for old_project, _manager_id in old_manager_projects
					if old_project.id != project_id
				]
				UserService.assign_projects(
					old_manager_id,
					ProjectAssignmentSchema.AssignProjectsRequest(
						project_ids=updated_old_project_ids,
					),
					admin_context,
					db,
				)

			if data.manager_id is not None and data.manager_id != old_manager_id:
				new_manager_projects = ProjectRepository.get_all_projects(
					{"user_id": data.manager_id, "user_role": "manager"},
					db,
				)
				updated_new_project_ids = [
					new_project.id
					for new_project, _manager_id in new_manager_projects
				]
				if project_id not in updated_new_project_ids:
					updated_new_project_ids.append(project_id)
				UserService.assign_projects(
					data.manager_id,
					ProjectAssignmentSchema.AssignProjectsRequest(
						project_ids=updated_new_project_ids,
					),
					admin_context,
					db,
				)
		return ProjectSchema.ProjectResponse.model_validate(project).model_copy(
			update={"manager_id": data.manager_id}
		)
