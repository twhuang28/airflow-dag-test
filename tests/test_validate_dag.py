"""
    Make sure you have the right path of AIRFLOW_HOME
"""
import os
import pytest
from airflow.models import DagBag


APPROVED_TAGS = {"orders"}


def get_import_errors():
    """
    Generate a tuple for import errors in the dag bag
    """

    dag_bag = DagBag(dag_folder="./dags", include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    # prepend "(None,None)" to ensure that a test object is always created even if it's a no op.
    return [(None, None)] + [
        (strip_path_prefix(k), v.strip()) for k, v in dag_bag.import_errors.items()
    ]

def get_dags():
    """
    Generate a tuple of dag_id, <DAG objects> in the DagBag
    """

    dag_bag = DagBag(dag_folder="./dags", include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


@pytest.mark.parametrize(
    "rel_path,rv", get_import_errors(), ids=[x[0] for x in get_import_errors()]
)
def test_file_imports(rel_path, rv):
    """Test for import errors on a file"""
    if rel_path and rv:
        raise Exception(f"{rel_path} failed to import with message \n {rv}")


@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    """
        test dag level parameters
    """
    assert dag.tags, f"{dag_id} in {fileloc} has no tags"
    if APPROVED_TAGS:
        assert not set(dag.tags) - APPROVED_TAGS


def test_task_trigger_rule():
    """
        test task level parameters
    """
    dag_bag = DagBag(dag_folder="./dags", include_examples=False)
    dag_test_example = dag_bag.dags['dag_test_example']
    apply_discount_ti = dag_test_example.get_task('apply_discount')
    assert apply_discount_ti.trigger_rule == 'all_success'


def test_task_dependency():
    """
        test task dependency
    """
    dag_bag = DagBag(dag_folder="./dags", include_examples=False)
    dag_test_example = dag_bag.dags['dag_test_example']
    apply_discount_ti = dag_test_example.get_task('create_table')
    sum_orders_plus_shipping_ti = dag_test_example.get_task('sum_orders_plus_shipping')
    assert apply_discount_ti.downstream_list == [sum_orders_plus_shipping_ti]
