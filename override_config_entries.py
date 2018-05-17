#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', required=True, help='Файл с настройками запуска')

args, unknown = parser.parse_known_args()

with open(args.config) as stream:
    config = yaml.safe_load(stream)

# override config parameters with command line arguments
cmdline_args = {}
for arg in unknown:
    if arg.startswith('--'):
        key, _, value = arg[2:].partition('=')
        cmdline_args[key] = value
    else:
        cmdline_args[key] = arg

for key, value in cmdline_args.items():
    conf = config
    for k in key.split('.')[:-1]:
        conf = conf.setdefault(k, {})
    conf[key.split('.')[-1]] = value
