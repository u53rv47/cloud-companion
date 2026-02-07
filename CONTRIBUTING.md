# Contributing to Cloud Companion

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd cloud-companion
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate  # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   ```

5. Start services with Docker Compose:

   ```bash
   docker-compose up -d
   ```

6. Run tests:
   ```bash
   pytest
   ```

## Code Standards

- **Formatting**: `black app/`
- **Linting**: `ruff check app/`
- **Type checking**: `mypy app/`
- **Tests**: `pytest tests/`

Run all checks:

```bash
pre-commit run --all-files
```

## Making Changes

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes and write tests
3. Ensure all tests pass: `pytest`
4. Submit a pull request

## Pull Request Process

- Provide clear description of changes
- Include tests for new functionality
- Update documentation as needed
- Ensure CI passes

## Reporting Issues

Use GitHub Issues with:

- Clear title and description
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details

## License

By contributing, you agree to license your code under Apache 2.0.
