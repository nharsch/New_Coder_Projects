from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc

class TalkBackBotFactory(protocol.ClientFactory):
    # instantiate the TalkBackBot IRC protocol

    def __init__(self, channel, nickname, realname, quotes, trigger):
        """Initialize the bot factory with our settings."""
        self.channel = channel
        self.nickname = nickname
        self.realname = realname
        self.quotes = quotes
        self.triggers = triggers

class TalkBackBot(irc.IRCClient):

    def connectionMade(self):
        """Called when a connection is made."""
        self.nickname = self.factory.nickname
        self.realname = self.factory.realname
        irc.IRCClient.connectionMade(self)
        log.msg("connectionMade")

    def connectionLost(self, reason):
        """Called when a connection is lost."""

    # callbacks for events

    def signedOn(self):
        """Called when bot has successfully signed on to server."""

    def joined(self, channel):
        """Called when the bot joins the channel."""

    def privmsg(self, user, channel, msg):
        """Called when the bot recieves a message."""

protocol = TalkBackBot


