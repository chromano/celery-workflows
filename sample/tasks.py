import time

from celery import Celery

app = Celery('', broker='redis://localhost/')

@app.task
def task0(*args, **kwargs):
    time.sleep(2)

@app.task
def task1(*args, **kwargs):
    time.sleep(2)

@app.task
def task2(*args, **kwargs):
    time.sleep(2)

@app.task
def task11(*args, **kwargs):
    time.sleep(2)
