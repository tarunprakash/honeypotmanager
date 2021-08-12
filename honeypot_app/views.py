import subprocess
import os
import json
import sys
import re
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Honeypot
from twisted.scripts.twistd import run
from channels.layers import get_channel_layer
from channels import layers
from asgiref.sync import async_to_sync
from honeypot_manager import ipManager

## get opencanary log filename from opencanary.conf
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(BASE_DIR, "../opencanary.conf")
with open(filepath, 'r') as file:
    config = json.load(file)
    LOG_FILEPATH = (config['logger']['kwargs']['handlers']['file']['filename'])

def index(request):
    with open(LOG_FILEPATH, 'r') as logfile:
        log = getLog(logfile)

    context = {
        "honeypots": Honeypot.objects.all(),
        "logs": log
    } 

    return render(request, "index.html", context)


def addHoneypot(request): 
    request = request.POST

    ## add to db
    Honeypot.objects.create(
        honeypotType = request['honeypotType'],
        honeypotIP = request['honeypotIP']
    )

    ## update config file
    with open(os.path.join(BASE_DIR, 'honeypot_manager/honeypot.conf'), 'w') as file:
        json.dump({
            "honeypotIP": request['honeypotIP'],
            "honeypotType": request['honeypotType']
        }, file)

    ## create honeypot
    pidFilename = f"{re.sub('[^0-9]', '', request['honeypotIP'])}_{request['honeypotType'].lower()}.pid"
    pidFilepath = os.path.join(BASE_DIR, f'process_ids/{pidFilename}')
    cmd = f"sudo twistd -y honeypot_app/honeypot_manager/createHoneypot.py --pidfile {pidFilepath}"
    subprocess.run(cmd.split())

    return HttpResponse("Done")


def removeHoneypot(request):
    request = request.POST

    ## remove from db
    Honeypot.objects.filter(
        honeypotType = request['honeypotType'],
        honeypotIP = request['honeypotIP']
    ).delete()

    ## remove IP alias
    ipManager.removeIp(request['honeypotIP'])

    ## get pid
    pidFilename = f"{re.sub('[^0-9]', '', request['honeypotIP'])}_{request['honeypotType'].lower()}.pid"
    pidFilepath = os.path.join(BASE_DIR, f'process_ids/{pidFilename}')
    cmd = f"sudo cat {pidFilepath}"
    pid = (subprocess.check_output(cmd.split())).decode('utf-8')

    ## kill process
    cmd = f"sudo kill {pid}"
    subprocess.run(cmd.split())

    return HttpResponse("Done")

@csrf_exempt
def updateLog(request):
    request = request.POST

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'logGroup',
        {
            'type': 'send_message',
            'message': request['msg']
        }
    )

    return HttpResponse('')


def getLog(f, lines=settings.LOG_ALERT_NUM, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    ## convert strings to dicts and reverse for time order
    return reversed([json.loads(line) for line in lines_found[-lines:]])