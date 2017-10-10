import os
import json

from celery.bin.base import Command

from .workflow import Workflow


class WorkflowsCommand(Command):
    supports_args = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--dag', required=True, help='The workflows JSON spec file')
        parser.add_argument(
            '--node', required=True,
            help='The task node name you want to start with')
        parser.add_argument(
            '--args',
            help='A JSON serialized string with the task args')

    def run(self, **kwargs):
        try:
            with open(kwargs['dag'], 'r') as fp:
                dag = json.load(fp)
        except FileNotFoundError:
            self.die('File not found: {}'.format(kwargs['dag']))
        except json.decoder.JSONDecodeError:
            self.die('Invalid JSON file: {}'.format(kwargs['dag']))

        if 'args' in kwargs:
            try:
                args = json.loads(kwargs['args'])
            except json.decoder.JSONDecodeError:
                self.die('Invalid JSON: {}'.format(kwargs['args']))
        else:
            args = []

        workflow = Workflow(dag)
        task = workflow.at(kwargs['node'])
        task_id = task.delay(*args)

        self.out('Task ID: {}'.format(task_id))
