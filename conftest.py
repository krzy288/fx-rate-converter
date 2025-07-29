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

@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context for Docker environment"""
    return {
        "ignore_https_errors": True,
        "bypass_csp": True,
    }

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Configure browser launch arguments for Docker environment"""
    return {
        "headless": True,
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
            "--allow-running-insecure-content",
            "--ignore-certificate-errors",
            "--ignore-ssl-errors",
            "--ignore-certificate-errors-spki-list",
            "--ignore-urlfetcher-cert-requests",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",
            "--disable-javascript",
            "--disable-default-apps",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--disable-background-networking",
            "--disable-backgrounding-occluded-windows",
            "--disable-client-side-phishing-detection",
            "--disable-default-apps",
            "--disable-hang-monitor",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-sync",
            "--disable-translate",
            "--metrics-recording-only",
            "--no-first-run",
            "--disable-ipc-flooding-protection"
        ]
    }
