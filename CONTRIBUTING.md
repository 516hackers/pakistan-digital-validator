
# Contributing to Pakistan Digital Validator

We love your input! We want to make contributing to Pakistan Digital Validator as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report bugs using Github's [issue tracker](https://github.com/516hackers/pakistan-digital-validator/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/516hackers/pakistan-digital-validator/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/pakistan-digital-validator.git
   cd pakistan-digital-validator
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

5. Run tests to ensure everything works:
   ```bash
   python -m pytest tests/
   ```

## Coding Standards

- Use Python 3.7+ compatible code
- Follow PEP 8 style guide
- Include type hints where possible
- Write docstrings for all public functions
- Add tests for new functionality
- Update documentation when changing features

## Testing

Before submitting a pull request, please ensure:

- All tests pass: `python -m pytest tests/`
- Code coverage is maintained: `python -m pytest --cov=src.pakistan_validator tests/`
- No linting issues: `pylint src/pakistan_validator/`

## Ethical Guidelines

Given the sensitive nature of this project, please adhere to:

- Never include real personal data in tests or examples
- Use synthetic data for testing
- Maintain privacy and security as top priorities
- Ensure all changes comply with ethical AI practices
- Document any potential security implications

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation if you're changing functionality
3. The PR should work for Python 3.7+
4. Add tests that demonstrate your changes work
5. Ensure all tests and checks pass

## License
By contributing, you agree that your contributions will be licensed under its MIT License.
