#clean __pycache__ with 'bash commands/clean_pyc.sh' in terminal
find . -name "*.py[co]" -delete
find . -type d -name "__pycache__" -delete