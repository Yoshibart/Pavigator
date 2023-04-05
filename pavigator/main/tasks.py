import random
import subprocess
from celery import shared_task,Celery
import json
import requests
from .api_key import api_key

app = Celery('tasks', broker='redis://localhost:6379')

@shared_task(name="update_database")
def run_database_process():
    print("Updating ........")
    command = ['/bin/bash', './update.sh', '&']
    subprocess.Popen(command)
