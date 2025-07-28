import os
import pytest
from dotenv import load_dotenv

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev")

def pytest_configure(config):
    env = config.getoption("--env")
    env_file = f".env.{env}"
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        print(f"Loaded env: {env_file}")
    else:
        print(f"Env file not found: {env_file}")

@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    print(f"Loaded BASE_URL: {url}")
    return url
