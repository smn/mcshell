import sys

import click

from twisted.python import log
from twisted.internet import reactor


@click.group()
def main():
    pass


@main.command()
@click.option('--endpoint', default='tcp:8022', type=str,
              help='The endpoint to listen on.')
@click.option('--logfile',
              help='Where to log output to.',
              type=click.File('a'),
              default=sys.stdout)
def run(endpoint, logfile):
    log.startLogging(logfile)
    log.msg('Running mcshelld on %s.' % (endpoint,))
    reactor.run()
