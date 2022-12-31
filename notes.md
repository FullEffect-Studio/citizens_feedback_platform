# To install dependencies specified in pyproject.toml
pip install -r pyproject.toml

# To run test
pytest --svv

# For coverage test check
pytest --svv --cov=citizen_feedback_platform --cov-report=term-missing