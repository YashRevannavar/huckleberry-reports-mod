---
trigger: always_on
---

# Python Project Standards & Rules

This document outlines the architectural patterns, coding standards, and development workflows for Python projects.

## 1. Project Architecture

### Modular Package Structure
- Organize code into a core directory (e.g., `backend/`).
- Use feature-based sub-packages (e.g., `check_requests/`, `big_query/`) rather than layer-based (e.g., `models/`, `views/`).
- Each sub-package should be self-contained, containing its own handlers, models, and services.
- Create a utilities/constants.py to import all the .env variables, Always in UPPER_CASE.

### Service & Handler Patterns
- **Handlers (`*_handler.py`)**: Contain the core, low-level logic or integration with external libraries (e.g., Selenium logic, spreadsheet parsing).
- **Services (`*_service.py`)**: Orchestrate handlers and provide a high-level API for the rest of the application.
- **Contracts (`contracts.py`)**: Use Abstract Base Classes (ABC) to define interfaces for core components, ensuring consistency across different implementations (e.g., `BaseCheck`).

### Data Modeling
- Use `@dataclass` for data transfer objects (DTOs) and internal models.
- Avoid raw dictionaries for passing complex data; prefer typed models.
- use Enums where required.
---

## 2. Coding Standards

### Naming Conventions
- **Modules/Packages**: `snake_case` (e.g., `data_handlers/`)
- **Functions/Variables**: `snake_case` (e.g., `run_request_check()`)
- **Classes**: `PascalCase` (e.g., `RequestCheckResult`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `STATUS_SUCCESS`)

### Typing & Documentation
- **Type Hinting**: Mandatory for all function signatures (arguments and return types).
- **Docstrings**: Provide a concise summary for all public classes and methods. Follow the Sphinx/reST style for parameters:
  ```python
  def example_function(param1: str) -> bool:
      """
      Summary of the function.
      :param param1: Description of param1.
      :return: Description of the return value.
      """
  ```

### Error Handling
- Use `try...except` blocks strategically to catch and log exceptions.
- Prefer returning "Result" objects that contain status and error information rather than letting exceptions bubble up to the entry point.
- Log errors with context: `logger.error(f"Failed to process {url}: {exc}")`.

---

## 3. Tooling & Quality Control

### Formatting & Linting
- **Black**: The standard for code formatting.
- **Flake8**: Use for linting (ignore `E501`, `W503`, `E266`).
- **Autoflake**: Automatically remove unused imports and variables.
- **Pre-commit**: Enforce these standards locally using pre-commit hooks.

### Logging
- Use a centralized logging configuration (e.g., `utilities/logging_config.py`).
- Suppress noisy logs from third-party libraries (Selenium, urllib3).
- Use structured log levels: `DEBUG` for verbose trace, `INFO` for progress, `WARNING` for non-critical failures, `ERROR` for critical issues.

---

## 4. Testing Strategy

### Framework & Structure
- Use the standard `unittest` library.
- Mirror the source code structure in the `tests/` directory.
- Test files must be prefixed with `test_` (e.g., `test_request_check.py`).

### Practices
- Implement `setUp()` and `tearDown()` for resource management (e.g., closing browser clients).
- Include "CI" tests that verify core functionality in a headless environment.
- Use descriptive assertion messages: `self.assertEqual(a, b, "Message describing why this failed")`.

---

## 5. Development Workflow

- **Virtual Environments**: Always use `.venv`.
- **Dependencies**: Maintain a clean `requirements.txt`.
- **Config Management**: Use `.env` files and `python-dotenv` for environment-specific variables.