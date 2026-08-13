from sqlalchemy import insert
from app.utils import security
from app import db
from app.db.database import Base, engine, SessionLocal

from app.models.UserModel import User
from app.models.ProjectModel import Project
from app.models.PasswordModel import Password
from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.RoleAssignmentModel import RoleAssignment
from app.models.RoleModel import Role, RoleEnum as RE
from app.models.TaskModel import Task
from app.models.TimeLogModel import TimeLog


print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

try:
    db = SessionLocal()
    print( "Creating default roles" )
    admin_role = Role( role = RE.ADMIN )
    manager_role = Role( role = RE.MANAGER )
    employee_role = Role( role = RE.EMPLOYEE )
    db.add( admin_role )
    db.add( manager_role )
    db.add( employee_role )
    db.flush()
    print( "Created roles successfully" )

    print( "Creating Default ADMIN" )
    user = User( 
        userid = "def_admin",
        name = "admin",
        company_mail = "defadmin@tektalis.com",
        phone_number = "1234567890"
    )
    db.add( user )
    db.flush()
    admin_user = db.query( User).filter( User.name == "admin" ).first()
    password = Password( 
        username = "defuser",
        password = security.hash_password( "abc123" ),
        user_id = admin_user.id
    )
    db.add( password )
    db.flush()
    print( "Created ADMIN successfully" )

    print( "Assigning roles" )
    roles = db.query( Role ).all()
    role_assignments = [
        { 
            "user_id": admin_user.id, "role_id": role.id
        }
        for role in roles
    ]
    db.execute(insert(RoleAssignment).values(role_assignments))
    print( "Assigned roles successfully" )
    db.commit()

    user_result = db.query( User).all()
    password_result = db.query( Password ).all()
    roles_result = db.query( Role ).all()
    role_assignment_result = db.query( RoleAssignment ).all()

    print( "user: ", user_result, "password: ", password_result, "roles: ", roles_result, "role_assignment: ", role_assignment_result, sep = "\n" )


except Exception as e:
    db.rollback()
    print( "error in default db setup:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", str( e ) )
finally:
    db.close()