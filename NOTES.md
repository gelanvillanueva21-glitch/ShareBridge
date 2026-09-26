# ShareBridge Journal

## Session Notes

**2026-09-26**
- **Learned/Agreed**: Acknowledged the Project Brief for ShareBridge (Local Donation Network).
- **Built**: Initialized project structure understanding. Created backend and frontend `.env` files.
- **Next Steps**: Awaiting the first prompt for the step-by-step build order (Project setup + base layout).


You are working on an enterprise-style FastAPI backend. Follow these rules for every response and code generation task.

Architecture Rules

* Use a strict Router → Service → Repository architecture.
* Routers only handle HTTP requests, responses, validation, dependency injection, and status codes.
* Services contain all business logic.
* Repositories only communicate with the database and perform database operations.
* Schemas act as validation and data contracts between layers.
* When a new business logic operation is introduced, create or extend a Service.
* When a new database operation is introduced, create or extend a Repository.
* Always check existing files first before creating new classes, services, repositories, dependencies, or utilities. Reuse existing code whenever possible.

Dependency Injection Rules

* Use typing.Annotated for all dependencies.
* Create reusable dependencies instead of repeating dependency logic.
* Shared dependencies should be centralized and reused across routers and services.
* Prefer dependency aliases for commonly used dependencies.

Naming Rules

* Use descriptive and readable names.
* Do not use cryptic abbreviations.
* Avoid names like:

  * db
  * session
  * repo
  * svc
  * usr
* Bad:

  * DBSession
  * db_session
  * user_svc
* Good:

  * DatabaseDepends
  * CurrentUserDepends
  * ProfileRepositoryDepends
  * AuthenticationServiceDepends

Exception:

* Shortened names are acceptable when the full name becomes excessively long and readability remains clear.
* Examples:

  * ProfileRepoDepends
  * CurrentUserDepends

Code Style Rules

* Leave 2 blank lines between top-level functions and classes.
* Keep function chains readable.
* Prioritize readability over shortening code.
* Use explicit variable names rather than abbreviations.
* Write code as if another developer will maintain it for years.

Project Design Principles

* Reuse before creating.
* Search existing services, repositories, schemas, dependencies, utilities, and models before generating new code.
* Avoid duplicate logic.
* Keep responsibilities separated:

  * Router = Request handling
  * Service = Business logic
  * Repository = Database access
  * Schema = Validation and contracts

Before generating code:

1. Identify whether the logic belongs to Router, Service, Repository, Schema, Dependency, or Utility.
2. Check if an existing implementation can be reused.
3. Extend existing code when appropriate.
4. Only create new files when necessary.
5. Follow all naming and architecture rules above.
6. Use SQLAlchemy Async patterns.
7. Use Annotated dependencies everywhere possible.
8. Prioritize maintainability, readability, and consistency over brevity.



Import Style Rules

* All imports must be placed at the top of the file.
* Group imports by category in the following order:

  1. Standard library imports
  2. Third-party package imports
  3. Local application imports
* Leave 2 blank lines between import groups.
* If an import section becomes large (approximately 5 or more imports in a group), add additional spacing to improve readability.
* Prefer multi-line imports when the imported names become too long or numerous.
* Keep imports organized alphabetically when practical.
* Remove unused imports.
* Never place imports inside functions unless there is a specific technical reason (e.g. avoiding circular imports or lazy loading).



Example:

```python
from typing import Annotated
from uuid import UUID


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.dependencies.database import DatabaseDepends
from app.dependencies.user import CurrentUserDepends
from app.schemas.profile import ProfileResponseSchema
from app.services.profile import ProfileService
```

The goal is to make large files easy to scan and maintain. Readability is preferred over minimizing vertical space.




<!-- Additions -->

- Use Typealias whenever using Annotated.




<!-- Function Parameter Formatting Rules -->

* If a function, method, class constructor, dependency, or function call contains more than 2 parameters, place each parameter on its own line.
* Do not keep long parameter lists on a single line.
* Always include a trailing comma on the last parameter when using multi-line formatting.
* Apply this rule consistently to:

  * Function definitions
  * Class constructors
  * Function calls
  * Dependency declarations
  * Object creation
  * SQLAlchemy queries when appropriate

Bad:

```python
async def create_profile(current_user: User, profile_service: ProfileService, profile_data: ProfileCreateSchema):
```

Good:

```python
async def create_profile(
    current_user: User,
    profile_service: ProfileService,
    profile_data: ProfileCreateSchema,
):
```

Bad:

```python
profile = Profile(first_name=data.first_name, last_name=data.last_name, user_id=current_user.id)
```

Good:

```python
profile = Profile(
    first_name=data.first_name,
    last_name=data.last_name,
    user_id=current_user.id,
)
```

Goal:

* Optimize readability over compactness.
* Make parameter additions and Git diffs cleaner.
* Keep function signatures easy to scan in large codebases.

