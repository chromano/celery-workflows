# workflows

This project goal is to make it easier to run Celery tasks
with dependency between them, which is called a workflow.

A workflow is defined outside of the task itself, through
a hash table with the following format:

    {
        "task1": {
            "task11" {
                "task111": {
                }
            },
            "task12": {
            }
        }
    }

That is, _task11_ and _task12_ will both execute at the
at same time after _task1_ is complete. Likewise, _task111_ 
will execute only after _task11_  completes.

## Installation

    $ pip install workflows

## Usage

    import json
    from workflows.workflow import Workflow

    dag = json.load(open('workflows.json'))

    Workflow(dag).at('task11').delay()

For the example above, consider the file _workflows.json_
contains the following contents:

    {"tasks1":{"tasks11":{"tasks111":{}},"tasks12":{}}}

That is the tasks DAG as introduced before.

It is also a good idea to have your workflows inside a file,
given the Celery command made available by this project where
you can start a workflow at any point through the command
line:

    $ celery workflows --dag=workflows.json --node=tasks11
