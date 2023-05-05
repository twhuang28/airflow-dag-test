from pendulum import datetime
from dags.dag_test_example import dag_test_example


if __name__ == "__main__":
    dag_object = dag_test_example()
    conn_path = "config/connections.yaml"
    variables_path = "config/variables.yaml"
    my_discount = 0.60

    dag_object.test(
        execution_date=datetime(2024, 1, 29),
        conn_file_path=conn_path,
        variable_file_path=variables_path,
        run_conf={"discount": my_discount},
    )
