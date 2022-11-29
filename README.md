# Airflow in local

Example of how to run Airflow in local, without Docker.

## Installation

(Optionnal) Install [conda](https://docs.conda.io/en/latest/miniconda.html) and create a conda environment. It will help you to handle several versions of Python on your computer:
```bash
# Example here for python 3.8
conda create -y -q --no-default-packages --name airflow_in_local_3.8 python=3.8 virtualenv invoke

conda activate airflow_in_local_3.8
```

Install python [invoke](https://www.pyinvoke.org/) lib:
```bash
pip install invoke
```

Install the project:
```bash
invoke install
```

## How to use

Run this command to run Airflow (scheduler + web server). The web server will be available on the address [http://127.0.0.1:8080](http://127.0.0.1:8080). The login/password is admin/admin.
To stop the server, press `Ctrl+c` or `Command+c`.
```bash
invoke start-airflow
```

Now you can start to create some DAGs in `src/` folder.