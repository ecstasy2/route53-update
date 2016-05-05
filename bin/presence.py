#!/usr/bin/env python

import argparse
import os
import signal
import sys
import time

import boto.route53

# example: route53.py \ 
# --name bob.example.com. \
# --type CNAME \
# --value alice.example.com \
# --zone example.com.
# NOTE: zone must end with full stop, and name must be FQDN, with full stop

parser = argparse.ArgumentParser(description='create dns record')
parser.add_argument('--access-key', metavar='<ACCESS_KEY>', default=os.environ.get('ACCESS_KEY'), help='AWS Access Key')
parser.add_argument('--secret-key', metavar='<SECRET_KEY>', default=os.environ.get('SECRET_KEY'), help='AWS Secret Key')
parser.add_argument('--name', metavar='<NAME>', default=os.environ.get('NAME'),
                    help='Name of DNS record')
parser.add_argument('--type', metavar='<TYPE>', default=os.environ.get('TYPE'),
                    help='Type of DNS record (A, CNAME, etc)')
parser.add_argument('--value', metavar='<VALUE>', default=os.environ.get('VALUE'),
                    help='Value of DNS record')
parser.add_argument('--zone', metavar='<ZONE>', default=os.environ.get('ZONE'),
                    help='Zone to add record to')
parser.add_argument('--ttl', metavar='<TTL>', default=300,
                    help='TTL of record')
args = parser.parse_args()

conn = boto.route53.Route53Connection(aws_access_key_id=args.access_key,aws_secret_access_key=args.secret_key)
zone = conn.get_zone(args.zone)

print "Creating record: {} {} {}".format(args.name, args.type, args.value)
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

oldrecord=zone.find_records(args.name,args.type)
zone.update_record(oldrecord,args.value)

print "Created."
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

