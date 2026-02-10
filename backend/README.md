# Create a virtual environment in this folder
`python3 -m venv venv`

# Activate it
`source venv/bin/activate`

# Install all dependencies by running
`pip install -r requirements.txt`

# Run the server
- Dev version `fastapi dev main.py`
- Prod version `fastapi run main.py`
- Version to run it in a way it's accessible in local network `uvicorn main:app --host 0.0.0.0 --reload` or `fastapi dev main.py --host 0.0.0.0`
