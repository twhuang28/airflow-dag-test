"""
    Ref: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
"""
import datetime

import pendulum
import pytest

from airflow import DAG
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.utils.types import DagRunType
from dags.custom_operator import MyBasicMathOperator

DATA_INTERVAL_START = pendulum.datetime(2021, 9, 13, tz="UTC")
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)

TEST_DAG_ID = "my_custom_operator_dag"
TEST_TASK_ID = "my_custom_operator_task"


@pytest.fixture()
def dag():
    with DAG(
        dag_id=TEST_DAG_ID,
        schedule="@daily",
        start_date=DATA_INTERVAL_START,
    ) as dag:
        op = MyBasicMathOperator(
            task_id=TEST_TASK_ID,
            first_number=3,
            second_number=5,
            operation="*",
            dag=dag
        )
    return dag


def test_my_basic_math_operator(dag):
    dagrun = dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=pendulum.now(),
        data_interval=(DATA_INTERVAL_START, DATA_INTERVAL_END),
        start_date=DATA_INTERVAL_END,
        run_type=DagRunType.MANUAL,
    )
    ti = dagrun.get_task_instance(task_id=TEST_TASK_ID)
    ti.task = dag.get_task(task_id=TEST_TASK_ID)
    ti.run(ignore_ti_state=True)
    assert ti.state == TaskInstanceState.SUCCESS
    # Assert something related to tasks results.

