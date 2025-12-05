import os


def test_env_example_exists():
    assert os.path.exists('.env.example')


def test_contributing_exists():
    assert os.path.exists('CONTRIBUTING.md')


def test_ci_workflow_exists():
    assert os.path.exists('.github/workflows/ci.yml')
