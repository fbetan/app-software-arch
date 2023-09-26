#!/usr/bin/env python3
import sys
import os
import pika
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///politicians.db'

conn = sqlite3.connect('database/politicians.db')
cur = conn.cursor()


def main():
    pikaconn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = pikaconn.channel()

    channel.queue_declare(queue='search')
    
    def callback(ch,method,properties,body):
        body = json.loads(body)
        print(f" [x] Received {body}")

    channel.basic_consume(queue='search',on_message_callback=callback,auto_ack=True)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    #on receipt of message

    channel.queue_declare(queue='parameters')


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    
