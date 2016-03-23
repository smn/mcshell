import sys

import click

from twisted.python import log
from twisted.internet import reactor
from twisted.internet.task import react

from .shell import Shell
from .client import Client


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


@main.command()
@click.option('--host', default='localhost', type=str,
              help='The host to connect to.')
@click.option('--port', default=22, type=int,
              help='The port to connect to.')
@click.option('--username', type=str)
@click.option('--keys', type=click.Path(exists=True), multiple=True,
              help='Which keys to connect with.')
@click.option('--known-hosts', type=click.Path(exists=True), default=None,
              help='Which known_hosts file to use.')
@click.option('--agent/--no-agent', default=True)
@click.option('--logfile',
              help='Where to log output to.',
              type=click.File('a'),
              default=sys.stdout)
def client(host, port, username, keys, known_hosts, agent, logfile):
    log.startLogging(logfile)
    log.msg('Connecting %s@%s:%s.' % (username, host, port,))

    client = Client(host, port, str(username), keys, known_hosts, agent)
    return react(lambda reactor: client.execute(b"/bin/cat"))
