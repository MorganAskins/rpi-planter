#!/bin/env python
from multiprocessing import Process
from datetime import datetime as dt
import time
import requests
import argparse
import json
import os
from sprinkler import Sprinkler


def parse_args():
    config_file = os.path.abspath(os.path.dirname(__file__)) + '/config.json'
    parser = argparse.ArgumentParser(description='Run sprinkler')
    parser.add_argument('-d', '--duration', type=int, default=45, help='Duration to run pump')
    parser.add_argument('--ignore_sensor', action='store_true', help='Ignore sensor reading')
    parser.add_argument('--config', type=str, default=config_file, help='Configuration file')
    return parser.parse_args()

def send_message(msg, to):
    data = {"content": msg}
    response = requests.post(to, data=data, timeout=5)
    return response


def main():
    args = parse_args()
    # Load configuration file
    with open(args.config) as f:
        config = json.load(f)

    sprinkler = Sprinkler(
        config['ultrasonic']['trigger'],
        config['ultrasonic']['echo'],
        config['relay']['pin'],
    )
    init_distance = 0 if args.ignore_sensor else sprinkler.read_volume()
    if init_distance < 5:
        send_message(f"Alert: low level detected ({init_distance:0.1f}%)", config['discord_hook'])
        exit(1)
    sprinkler.run_pump(args.duration)
    new_distance = 0 if args.ignore_sensor else sprinkler.read_volume()
    timenow = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'{timenow} ({args.duration}s Fill) from {init_distance:0.1f}% -> {new_distance:0.1f}%\n'

    file_path = os.path.abspath(os.path.dirname(__file__)) + '/log.txt'
    with open(file_path, 'a') as outfile:
        outfile.write(msg)

    rsp = send_message(msg, config['discord_hook'])


if __name__ == '__main__':
    args = parse_args()
    with open(args.config) as f:
        config = json.load(f)
    ## Add timeout if no response
    timeout = 120
    p1 = Process(target=main)
    p1.start()
    p1.join(timeout)
    if p1.is_alive():
        p1.terminate()
        send_message("Error: Timeout", config['discord_hook'])
        exit(1)
    exit(0)
