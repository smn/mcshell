import os
import getpass

from twisted.internet import reactor
from twisted.conch.endpoints import SSHCommandClientEndpoint
from twisted.conch.client.knownhosts import KnownHostsFile
from twisted.conch.ssh.keys import Key, EncryptedKeyError
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.defer import Deferred
from twisted.python.filepath import FilePath


class NoiseProtocol(Protocol):
    def connectionMade(self):
        self.finished = Deferred()
        self.strings = ["bif", "pow", "zot"]
        self.sendNoise()

    def sendNoise(self):
        if self.strings:
            self.transport.write(self.strings.pop(0) + "\n")
        else:
            self.transport.loseConnection()

    def dataReceived(self, data):
        print "Server says:", data
        self.sendNoise()

    def connectionLost(self, reason):
        self.finished.callback(None)


def read_key(path):
    try:
        return Key.fromFile(path)
    except EncryptedKeyError:
        passphrase = getpass.getpass("%r keyphrase: " % (path,))
        return Key.fromFile(path, passphrase=passphrase)


class Client(object):

    clock = reactor

    def __init__(self, host, port, username, keys, known_hosts,
                 agent=False):
        self.host = host
        self.port = port
        self.username = username
        self.keys = [read_key(key) for key in keys]
        self.known_hosts = (KnownHostsFile.fromPath(FilePath(known_hosts))
                            if known_hosts else None)
        if agent:
            self.agent_endpoint = UNIXClientEndpoint(
                self.clock, os.environ["SSH_AUTH_SOCK"])
        else:
            self.agent_endpoint = None

    def execute(self, command):
        print 'command %r' % (command,)
        endpoint = SSHCommandClientEndpoint.newConnection(
            self.clock, command, self.username, self.host,
            port=self.port, keys=self.keys,
            agentEndpoint=self.agent_endpoint,
            knownHosts=self.known_hosts)

        factory = Factory()
        factory.protocol = NoiseProtocol

        d = endpoint.connect(factory)
        d.addCallback(lambda proto: proto.finished)
        return d
