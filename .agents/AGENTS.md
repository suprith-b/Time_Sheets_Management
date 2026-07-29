# Project Coding Guidelines

- **Coding Style**: Keep code minimal, clean, simple, and direct. Avoid unnecessary complications or over-engineering. Draw style inspiration from `time_sheets_management`. Try to reuse exisiting functionalities and methods to avoid code repetition.
- **Response Schemas**: Every Pydantic response schema MUST include `model_config = ConfigDict(from_attributes=True)`.
- **No Defensive Type Checks**: Assume inputs and objects passed across layers are already in correct formats/types. Do not add runtime type checking code (e.g., checking if an argument is `list`, `dict`, or `str`).
- **Use Enums Directly**: Use `RoleEnum` and standard Enum classes directly in schemas, query parameters, and database filters instead of manual lowercasing or custom string mapping functions.
- **Clean Database Queries**: Write straightforward, single-pass SQLAlchemy queries without unnecessary subqueries, redundant iterations, or duplicate lookups.
- **Layer Responsibilities**:
  - **Controllers**: Keep minimal with input declaration and authorization/role validations (`RoleValidation.validate_role`).
  - **Services**: Contain business logic and DTO mappings using Pydantic schemas. Should not directly interact with Database.
  - **Repositories**: Direct, concise database operations.
- **Code Reuse**: Try to reuse existing functions and methods as much as possible to avoid code repetition.

