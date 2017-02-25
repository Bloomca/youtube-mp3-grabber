# 1. allow subscription to the channel
# 2. get all subscriptions, get their last Update Date and get all videos from it
# 3. get all videos and convert them to
# 4. upload to needed storage (oneDrive for now), add adapters to many

import datetime

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from terminaltables import AsciiTable
from db import Subscription, Base
from youtube import processVideos

engine = create_engine('sqlite:///youtube-grabber.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@click.command()
@click.option('--channel', help='channel id in youtube')
@click.option('--name', help='name to prefix in files')
@click.option('--key', help='YouTube API key')
@click.argument('command')
def start_application(channel, command, name, key):
    if command == 'subscribe':
        subscribe(channel, name)
    if command == 'unsubscribe':
        unsubscribe(channel)
    if command == 'show':
        show()
    if command == 'update':
        update(key)

def update(key):
    session = DBSession()
    subscriptions = session.query(Subscription).all()
    for sub in subscriptions:
        processVideos(sub, key)
        sub.fetchedBefore = generate_timestamp()
    session.commit()

def generate_timestamp():
    d = datetime.datetime.utcnow() # <-- get time in UTC
    return d.isoformat("T") + "Z"

def subscribe(channel, name):
    session = DBSession()
    timestamp = generate_timestamp()
    subscription = Subscription(channel=channel, fetchedBefore=timestamp, name=name)
    session.add(subscription)
    session.commit()
    click.echo('channel was successfully added')

def unsubscribe(channel):
    pass

def show():
    session = DBSession()
    subscriptions = session.query(Subscription).all()

    result = [['ID', 'CHANNEL', 'NAME', 'TIME']]
    for sub in subscriptions:
        result.append([sub.id, sub.channel, sub.name, sub.fetchedBefore])

    table = AsciiTable(result)
    click.echo(table.table)

if __name__ == '__main__':
    start_application()
