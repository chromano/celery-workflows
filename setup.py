from setuptools import setup

setup(
    name='celery-workflows',
    version='0.0.1',
    packages=['workflows'],
    entry_points={
        'celery.commands': [
           'workflows = workflows.command:WorkflowsCommand',
        ],
    },
)
