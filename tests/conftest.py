import pytest
from testcontainers.compose import DockerCompose


@pytest.fixture(scope='session', autouse=True)
def setup_docker_compose():
    with DockerCompose(
        "./",
        compose_file_name=["docker-compose.yaml"],
        pull=True
    ) as compose:
        stdout, stderr = compose.get_logs()
        if stderr:
            print("Errors\\n:{}".format(stderr))
        yield compose
