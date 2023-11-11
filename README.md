## Dev environment setup
## To run via docker

```
docker compose build
docker compose up
```


## To run locally without docker
### Prerequisites
- Python 3.x installed on your system.
- Pip (Python package manager) installed.
- The provided example code utilizes SQLite as the database engine, eliminating the need for additional database setup.

### Step 1: Create a Virtual Environment

```
python3 -m virtualenv env_name
```

### Step 2: Activate the Virtual Environment
```
source venv/bin/activate
```
### Step 3: Install Project Dependencies
```
pip install -r requirements.txt
```
### Step 4: Set Up the Database
The provided example code utilizes SQLite as the database engine, eliminating the need for additional database setup.
```
./manage.py migrate
```
### Step 5: Start the Django Server
```
./manage.py runserver
```

Import the Postman collections and send requests to the desired endpoints.



