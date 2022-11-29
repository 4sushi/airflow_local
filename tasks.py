# Author: 4sushi
from invoke import task
import shutil
import os 


# Global variables
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PYTHON_VERSION = '3.8'
VENV_PATH = os.path.join(CURRENT_PATH, 'venv')
VENV_PYTHON_PATH = os.path.join(VENV_PATH, 'bin', 'python')
AIRFLOW_VERSION = '2.4.3'
AIRFLOW_SERVER_PORT = '8080'
AIRFLOW_HOME = os.path.join(CURRENT_PATH, '.airflow')


# Set environment variables
os.environ['AIRFLOW_HOME'] = AIRFLOW_HOME
os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = os.path.join(CURRENT_PATH, 'src')
os.environ['AIRFLOW__CORE__LOAD_EXAMPLES'] = 'False'
os.environ['AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL'] = '10'
os.environ['AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT'] = 'False'


@task
def test(c):
    c.run(f'{VENV_PYTHON_PATH} -m airflow scheduler')

@task
def install(c):
    """
    Install project:
    - Create virtual environment
    - Install dependancies
    - Init airflow
    """
    shutil.rmtree(VENV_PATH, ignore_errors=True)
    shutil.rmtree(AIRFLOW_HOME, ignore_errors=True)
    os.makedirs(AIRFLOW_HOME)
    c.run(f'python -m virtualenv -p python3 {VENV_PATH}')
    c.run(f'{VENV_PYTHON_PATH} -m pip install -U -q pip')
    constraint_url = f'https://raw.githubusercontent.com/apache/airflow/constraints-{AIRFLOW_VERSION}/constraints-{PYTHON_VERSION}.txt'
    c.run(f'{VENV_PYTHON_PATH} -m pip install "apache-airflow=={AIRFLOW_VERSION}" --constraint "{constraint_url}"')
    c.run(f'{VENV_PYTHON_PATH} -m pip install -U -q -r requirements.txt')
    c.run(f'{VENV_PYTHON_PATH} -m airflow db init')
    c.run(f'{VENV_PYTHON_PATH} -m airflow users create --username admin --password admin --firstname admin \
            --lastname admin --role Admin --email admin@airflow.org')


@task
def update(c):
    """
    Install dependancies from requirements.txt file
    """
    c.run(f'{VENV_PYTHON_PATH} -m pip install -U -q -r requirements.txt')


@task
def start_airflow(c):
    """
    Start Airflow scheduler & web server
    Press Ctrl+c or Command+c to quit 
    """
    c.run(f'{VENV_PYTHON_PATH} -m airflow scheduler &', asynchronous=True)
    c.run(f'{VENV_PYTHON_PATH} -m airflow webserver --port {AIRFLOW_SERVER_PORT}')