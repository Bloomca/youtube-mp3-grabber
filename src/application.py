import datetime

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from terminaltables import AsciiTable
from db import Subscription, Base
from youtube import process_videos

@click.command()
@click.option('--channel', help='channel id in youtube')
@click.option('--name', help='name to prefix in files')
@click.option('--key', help='YouTube API key')
@click.argument('command')
def start_application(channel, command, name, key):
    """
    Start CLI application with needed options and command
    """
    engine = create_engine('sqlite:///youtube-grabber.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    
    if command == 'subscribe':
        subscribe(channel, name, DBSession)
    if command == 'unsubscribe':
        unsubscribe(channel)
    if command == 'show':
        show(DBSession)
    if command == 'update':
        update(key, DBSession)

def update(key, DBSession):
    """
    Get all subscriptions from db, and try to get all new
    episodes out there. If found any, process videos and
    set new fetchedBefore timestamp
    """
    session = DBSession()
    subscriptions = session.query(Subscription).all()
    for sub in subscriptions:
        process_videos(sub, key)
        sub.fetchedBefore = generate_timestamp()
    session.commit()

def generate_timestamp():
    """Current datetime in rfc 3339 (for youtube date)"""
    utc_date = datetime.datetime.utcnow() # <-- get time in UTC
    return utc_date.isoformat("T") + "Z"

def subscribe(channel, name, DBSession):
    """subscribe to the channel with given name"""
    session = DBSession()
    timestamp = generate_timestamp()
    subscription = Subscription(channel=channel, fetchedBefore=timestamp, name=name)
    session.add(subscription)
    session.commit()
    click.echo('channel was successfully added')

def unsubscribe(channel):
    """unsubscribe from the channel with the given ID"""
    pass

def show(DBSession):
    """Show all your subscriptions in ASCII table"""
    session = DBSession()
    subscriptions = session.query(Subscription).all()

    result = [['ID', 'CHANNEL', 'NAME', 'TIME']]
    for sub in subscriptions:
        result.append([sub.id, sub.channel, sub.name, sub.fetchedBefore])

    table = AsciiTable(result)
    click.echo(table.table)

if __name__ == '__main__':
    start_application()
