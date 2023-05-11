# How to test dags?
### Why we need to test dags?
* To ensure that dags are supposed to work
* Allow colleagues to better verify that the dags are correct

### How to test dags
* [Test dags setup](./tests/test_validate_dag.py)
* [Test customized operators](./tests/test_operator.py)
* [Test dags run](./tests/test_run_dag.py)

### How to use this repository

1. Clone the repository.
2. Make sure you are in an environment that has Airflow 2.5+ installed by running `airflow version` from your command line.
3. If you use `virtualenv` you can run the following commands:
    ```sh
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    docker-compose up -d
    ```
4. Run `python run_dag.py`.
5. Run `python -m pytest tests/`.

### Relevant resources

- [Concept guide: Test Airflow DAGs](https://docs.astronomer.io/learn/testing-airflow)
- Airflow Documentation: [Testing DAGs with dag.test()](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html)
- Python Documentation: [The Python Debugger](https://docs.python.org/3/library/pdb.html)
- [How to install Airflow locally](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- Concept guide: [Custom Hooks and Operators](https://docs.astronomer.io/learn/airflow-importing-custom-hooks-operators)
- [Source code dag object](https://github.com/apache/airflow/blob/main/airflow/models/dag.py)
- [Debugging in VSCode](https://code.visualstudio.com/docs/editor/debugging)
