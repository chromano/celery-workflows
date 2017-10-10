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

## Sample

You can try this out by cloning this repository and using the
tasks and workflows file within the _sample_ directory:

    $ git clone git@github.com:chromano/celery-workflows.git
    $ cd celery-workflows/sample
    $ celery -A tasks worker -l INFO

Then in another terminal (within the same directory):

    $ python setup.py develop
    $ celery -A tasks workflows --dag=workflows.json \
        --node=tasks.task0

You'll need celery >= 4.0.2 and celery[redis] installed for
this to work.

The expected output from Celery would be along these lines:

    [2017-10-10 07:26:23,865: INFO/MainProcess] Received task: tasks.task0[d2d7eca0-d01f-4843-8029-fe8a956e53d7]
    [2017-10-10 07:26:25,871: INFO/MainProcess] Received task: tasks.task1[7cb300ec-6cc6-459e-89ed-d6d170c39d09]
    [2017-10-10 07:26:25,871: INFO/ForkPoolWorker-2] Task tasks.task0[d2d7eca0-d01f-4843-8029-fe8a956e53d7] succeeded in 2.0049495970015414s: None
    [2017-10-10 07:26:25,872: INFO/MainProcess] Received task: tasks.task2[ea25f93b-dd35-4057-b480-099f2ad12e28]
    [2017-10-10 07:26:27,876: INFO/ForkPoolWorker-1] Task tasks.task1[7cb300ec-6cc6-459e-89ed-d6d170c39d09] succeeded in 2.002907618007157s: None
    [2017-10-10 07:26:27,877: INFO/MainProcess] Received task: tasks.task11[fdc87d1b-001d-4594-a168-f1cdc009735d]
    [2017-10-10 07:26:27,876: INFO/ForkPoolWorker-3] Task tasks.task2[ea25f93b-dd35-4057-b480-099f2ad12e28] succeeded in 2.0012166789965704s: None
    [2017-10-10 07:26:29,881: INFO/ForkPoolWorker-4] Task tasks.task11[fdc87d1b-001d-4594-a168-f1cdc009735d] succeeded in 2.001783346000593s: None

Notice the order the tasks were executed, they are supposed
to follow the order defined in the workflows file.
