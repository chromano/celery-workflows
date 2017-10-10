"""This module provides resources for dealing with a workflow data
structure.

A workflow data structure must be a DAG in the following format:

    {
        'task0': {
            'task01': {
                'task011'
            },
            'task02': {
            }
        }
    }

Where each key consists of a Celery task name previously defined in
your application. Keys within the same level are ran simulatenously.

For the example above, starting the task0 would run task0 and once
completed it'll run task01 and task02 at the same time. Once task01
is completed, then task011 is run.
"""
from celery import group, signature


class Workflow():
    """Interface for a DAG representing your tasks (the `dag` parameter).

    The data structure can have shorter task names if a prefix is
    given through the `prefix` parameter.

    Workflow({
        'charge': {
            'dispatch_items': {
                'notify_dispatch'
            },
            'notify_payment': {
            }
        }
    }, prefix='checkout')

    You can use the above if your tasks are named, for example,
    `checkout.charge` or `checkout.dispatch`.
    """
    def __init__(self, dag, prefix=None):
        self.dag = dag
        self.prefix = prefix if prefix is not None else ''

    def at(self, node):
        """Given a node name which belongs to this instance's DAG,
        creates a tasks chain starting at the given node.

        workflow = Workflow({
            'charge': {
                'dispatch_items': {
                    'notify_dispatch'
                },
                'notify_payment': {
                }
            }
        }, prefix='checkout')

        Given the workflow instance above, you are able to run it
        starting at a specific node/task.

        You can use `workflow.at('charge')` to build a chain that
        will execute like this:

                           +----------------+    +-----------------+
                      .--> | dispatch_items | -> | notify_dispatch |
        +--------+   /     +----------------+    +-----------------+
        | charge | -:
        +--------+   \     +----------------+
                      `--> | notify_payment |
                           +----------------+

        Or `workflow.at('dispatch_items')` to remove the tasks
        `charge` and `notify_payment` from the tasks chain.

        This is specially useful when dealing with a broken workflow
        (when one or more nodes of a DAG failed to execute).
        """
        Q = [self.dag]

        while len(Q) > 0:
            top = Q.pop(0)
            if node in top.keys():
                start = top[node]
                break
            else:
                Q.extend(top.values())
        else:
            raise ValueError('Could not find node {}'.format(node))

        task_id = lambda name: '.'.join(
            filter(lambda value: len(value) > 0, (self.prefix, name)))

        def _graph(nodes, task):
            subtasks = []
            for name in nodes.keys():
                subtask = signature(task_id(name))
                if nodes[name]:
                    _graph(nodes[name], subtask)
                subtasks.append(subtask)

            task.link(group(subtasks))

            return task

        return _graph(start, signature(task_id(node)))
