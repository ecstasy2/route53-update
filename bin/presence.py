#!/usr/bin/env python

import argparse
import os
import signal
import sys
import time
import subprocess

import boto.route53

# example: route53.py \
# --name bob.example.com. \
# --type CNAME \
# --private should we assign the private ip? \
# --zone example.com.
# NOTE: zone must end with full stop, and name must be FQDN, with full stop

def str2bool(v):
  #susendberg's function
  return v.lower() in ("yes", "true", "t", "1")

parser = argparse.ArgumentParser(description='create dns record')
parser.add_argument('--access-key', metavar='<ACCESS_KEY>', default=os.environ.get('ACCESS_KEY'), help='AWS Access Key')
parser.add_argument('--secret-key', metavar='<SECRET_KEY>', default=os.environ.get('SECRET_KEY'), help='AWS Secret Key')
parser.add_argument('--name', metavar='<NAME>', default=os.environ.get('NAME'),
                    help='Name of DNS record')
parser.add_argument('--type', metavar='<TYPE>', default=os.environ.get('TYPE'),
                    help='Type of DNS record (A, CNAME, etc)')
parser.add_argument('--private', metavar='<PRIVATE_IP>', default=os.environ.get('PRIVATE_IP'),
                    help='Should we use the private ip address of the host?')

parser.add_argument('--zone', metavar='<ZONE>', default=os.environ.get('ZONE'),
                    help='Zone to add record to')
parser.add_argument('--ttl', metavar='<TTL>', default=300,
                    help='TTL of record')
args = parser.parse_args()

conn = boto.route53.Route53Connection(aws_access_key_id=args.access_key,aws_secret_access_key=args.secret_key)
zone = conn.get_zone(args.zone)

ip_addr = None
cmd = "curl -m 2 http://169.254.169.254/latest/meta-data/public-ipv4"

if str2bool(args.private):
    cmd = "curl -m 2 http://169.254.169.254/latest/meta-data/private-ipv4"

process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
ip_addr = process.communicate()[0]

print "Creating record: {} {} {}".format(args.name, args.type, ip_addr)
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

oldrecord=zone.find_records(args.name,args.type)

# TODO: Enable this
zone.update_record(oldrecord,ip_addr)

print "Created."
# the print above sometimes doesnt flush until container stops
sys.stdout.flush()

while True:
    print "Keep waiting forever."
    time.sleep(60)  # Delay for 1 minute (60 seconds)
