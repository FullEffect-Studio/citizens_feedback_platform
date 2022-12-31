### To install dependencies specified in pyproject.toml
pip install -r pyproject.toml

### To run test
pytest --svv

### For coverage test check
pytest --svv --cov=citizen_feedback_platform --cov-report=term-missing

### Notes on running wsgi.py
On Linux
- FLASK_CONFIG="development"flask run -h "0.0.0.0"

On windows
- SET FLASK_CONFIG=development
- flask run --extra-files / --debugger --reload

