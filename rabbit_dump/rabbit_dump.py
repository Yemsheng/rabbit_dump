#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import traceback
import json

import pika


DATA = []


def publish(host, port, exchange, routing_key, data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port))
    main_channel = connection.channel()
    for body in data:
        main_channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=body)
    connection.close()


def callback(ch, method, properties, body):
    DATA.append(body)


def consume(host='localhost', port=None, queue=None):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()
    try:
        channel.basic_consume(callback, queue=queue, no_ack=True)
    except Exception, e:
        print e
        print traceback.format_exc()
    connection.close()


def persistence(filename, data):
    try:
        data = json.dumps(data)
        f = file(filename, 'w')
        f.write(data)
        f.close()
    except Exception, e:
        print e
        print traceback.format_exc()


def parseArgument():
    parser = argparse.ArgumentParser()
    val = parser.add_argument('--host')
    val = parser.add_argument('--port')
    val = parser.add_argument('--queue', required=True)
    val = parser.add_argument('--file', required=True)
    val = parser.add_argument('--exchange', required=True)
    val = parser.add_argument('--routingkey', required=True)
    args = parser.parse_args()
    if args.port:
        args.port = int(args.port)

    return args


def main():
    args = parseArgument()
    consume(args.host, args.port, args.queue)
    persistence(args.file, DATA)
    publish(args.host, args.port, args.exchange, args.routingkey, DATA)


if __name__ == "__main__":
    main()
