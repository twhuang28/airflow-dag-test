import json
from airflow.models import Variable
from pendulum import datetime
from airflow.decorators import dag, task
# from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from dags.custom_operator import MyBasicMathOperator


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    # render Jinja template as native Python object
    render_template_as_native_obj=True,
    params={"discount": 1},
)
def dag_test_example():

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_default",
        sql="""
            DROP TABLE IF EXISTS orders;
            CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            values NUMERIC NOT NULL);
            INSERT INTO orders (values) VALUES (10), (20), (30), (40), (50);
        """,
    )

    @task
    def sum_orders_plus_shipping():
        shipping_cost = Variable.get("shipping_cost")["value"]
        pg_hook = PostgresHook.get_hook("postgres_default")
        conn = pg_hook.get_conn()
        with conn.cursor() as cur:
            cur.execute(f"SELECT values FROM orders;")
            order_values = cur.fetchall()
            order_values = [row[0].__float__() for row in order_values]
        # breakpoint()
        return sum(order_values) + shipping_cost

    apply_discount = MyBasicMathOperator(
        task_id="apply_discount",
        first_number="{{ ti.xcom_pull(task_ids='sum_orders_plus_shipping', key='return_value') }}",
        second_number="{{ params.discount }}",
        operation="*",
    )
    
    create_table >> sum_orders_plus_shipping() >> apply_discount
