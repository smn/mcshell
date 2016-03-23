from twisted.cred import portal
from twisted.conch import manhole_ssh, manhole_tap
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.python.filepath import FilePath
from twisted.internet.endpoints import serverFromString
from twisted.internet import reactor


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


class Shell(object):

    clock = reactor

    def __init__(self, twisted_endpoint, authorized_keys=None):
        self.twisted_endpoint = twisted_endpoint
        self.authorized_keys = authorized_keys

    def start(self):
        checker = SSHPubKeyDatabase(self.authorized_keys)
        ssh_realm = manhole_ssh.TerminalRealm()
        ssh_realm.chainedProtocolFactory = manhole_tap.chainedProtocolFactory({
            'foo': 'foo',
        })
        ssh_portal = portal.Portal(ssh_realm, [checker])
        factory = manhole_ssh.ConchFactory(ssh_portal)
        endpoint = serverFromString(self.clock, self.twisted_endpoint)
        return endpoint.listen(factory)
