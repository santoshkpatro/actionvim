# Contributing to ActionVim

Thank you for your interest in contributing to ActionVim! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- [uv](https://docs.astral.sh/uv/) (Python package installer)

### Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/santoshkpatro/actionvim.git
   cd actionvim
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   uv pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Setup database**

   ```bash
   python3 manage.py migrate
   ```

5. **Create superuser (optional)**

   ```bash
   python3 manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python3 manage.py runserver
   ```

## Making Changes

1. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Write clean, readable code
   - Follow Django conventions
   - Add tests for new features

3. **Run tests**

   ```bash
   pytest
   ```

4. **Check coverage**

   ```bash
   pytest --cov=actionvim
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

## Testing

We use pytest for testing. All tests should pass before submitting a pull request.

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=actionvim

# Generate coverage report
pytest --cov=actionvim --cov-report=html
```

### Writing Tests

- Write tests for all new functionality
- Place tests in the `tests/` directory
- Use descriptive test names
- Include both positive and negative cases

Example test:

```python
import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    assert user.username == 'testuser'
```

## Dependency Management

We use `uv` for managing dependencies. When adding or updating dependencies:

### Adding Development Dependencies

Add the dependency to `pyproject.toml` under the `[dependency-groups.dev]` section, then run:

```bash
uv pip compile pyproject.toml -o requirements-dev.txt --group dev
```

### Adding Production Dependencies

Add the dependency to `pyproject.toml` under the `[project.dependencies]` section, then run:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Keep functions small and focused
- Add docstrings for complex functions

## Pull Request Process

1. **Before submitting:**

   - Ensure all tests pass: `pytest`
   - Check test coverage: `pytest --cov=.`
   - Make sure code follows style guidelines

2. **Submit pull request:**

   - Use clear, descriptive title
   - Describe what your changes do
   - Reference any related issues

3. **After submission:**
   - Respond to feedback
   - Make requested changes
   - Keep your branch updated

## Commit Message Format

Use clear, descriptive commit messages:

```
type: brief description

Examples:
feat: add user authentication
fix: resolve login redirect issue
docs: update README installation steps
test: add tests for user model
```

## Reporting Issues

When reporting bugs, include:

- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)
- Environment details

## Getting Help

- Check existing issues and documentation
- Ask questions in GitHub discussions
- Be respectful and patient

Thank you for contributing to ActionVim!
