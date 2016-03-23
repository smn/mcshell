from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.conch.insults import insults
from twisted.python.filepath import FilePath
from twisted.internet.endpoints import serverFromString
from twisted.internet import reactor
from twisted.python import log


class SSHPubKeyDatabase(SSHPublicKeyDatabase):
    """
    Checker for authorizing people against a list of `authorized_keys` files.
    If nothing is specified then it defaults to `authorized_keys` and
    `authorized_keys2` for the logged in user.
    """
    def __init__(self, authorized_keys=None):
        self.authorized_keys = authorized_keys

    def getAuthorizedKeysFiles(self, credentials):
        if self.authorized_keys is not None:
            return [FilePath(ak) for ak in self.authorized_keys]

        return SSHPublicKeyDatabase.getAuthorizedKeysFiles(self, credentials)


class ShellProtocol(insults.TerminalProtocol):

    # defaults
    width = 80
    height = 24

    def terminalSize(self, width, height):
        self.width = width
        self.height = height


class ShellSession(manhole_ssh.TerminalSession):

    def execCommand(self, proto, cmd):
        log.msg('Asked to run: %s for %s.' % (cmd, proto))
        proto.write('You asked me to run: %s\n' % (cmd,))

    def windowChanged(self, dimensions):
        pass


class ShellUser(manhole_ssh.TerminalUser):
    pass


class ShellRealm(manhole_ssh.TerminalRealm):
    userFactory = ShellUser
    sessionFactory = ShellSession


class Shell(object):

    clock = reactor

    def __init__(self, twisted_endpoint, authorized_keys=None):
        self.twisted_endpoint = twisted_endpoint
        self.authorized_keys = authorized_keys

    def chainedProtocolFactory(self):
        return insults.ServerProtocol(ShellProtocol)

    def start(self):
        checker = SSHPubKeyDatabase(self.authorized_keys)
        ssh_realm = ShellRealm()
        ssh_realm.chainedProtocolFactory = self.chainedProtocolFactory
        ssh_portal = portal.Portal(ssh_realm, [checker])
        factory = manhole_ssh.ConchFactory(ssh_portal)
        endpoint = serverFromString(self.clock, self.twisted_endpoint)
        return endpoint.listen(factory)
