#!/usr/bin/python3

import sync_all
from time import sleep
from daemonize import Daemonize
import sys

pid=sync_all.getpid() #/tmp/test.pid

def main():
    while True:
        sleep(5)
        sync_all.action() #порядок

daemon = Daemonize(app="sync_all", pid=pid, action=main)
daemon.start()

