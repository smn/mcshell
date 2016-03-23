import sys

import click

from twisted.python import log
from twisted.internet import reactor

from .shell import Shell


@click.group()
def main():
    pass


@main.command()
@click.option('--endpoint', default='tcp:8022', type=str,
              help='The endpoint to listen on.')
@click.option('--authorized-keys', default=None,
              type=click.Path(exists=True), multiple=True,
              help=('Which files to use as authorized keys for SSH access. '
                    'This defaults to the current users\' authorized_keys.'))
@click.option('--logfile',
              help='Where to log output to.',
              type=click.File('a'),
              default=sys.stdout)
def run(endpoint, authorized_keys, logfile):
    log.startLogging(logfile)
    log.msg('Running mcshelld on %s.' % (endpoint,))

    shell = Shell(str(endpoint), authorized_keys)
    shell.start()

    reactor.run()
