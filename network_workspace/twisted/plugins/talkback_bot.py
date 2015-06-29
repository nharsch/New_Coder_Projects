from ConfigParser import ConfiParser

from twisted.application.service import IServiceMaker, service
from twisted.internet.endpoints import clientFromString
from twisted.plugin import IPlugin
from twisted.python import useage, log
from zope.interface iimport implementer

from talkback.bot import TalkBackotFactory
from talkback.quaote_picker import QuatePicker

class TalkBackBotService(Service):

    def __init__(self, endpoint, channel, nickname, realname, quotesFilename, triggers):

    def startService(self):
        """Contruct a client & connect to server."""

    def stopService(self):
        """Disconnect."""

@implementer(IserviceMaker, IPlugin)
class BotServiceMaker(object):
    tapname = "twsrs"
    description = "IRC bot that provides quotations from notable women"
    options = Options

    def makeService(self, options):
        """Construct the talkbackbot service."""
        config = ConfigParser()
        config.read([options['config']])
        triggers = [
            trigger.strip()
            for trigger in config.get('talkback', 'triggers').split('\n')
            if trigger.strip()
        ]

        return TalkBackBotService(
            endpoint=config.get('irc', 'endpoint'), 
            channel=config.get('irc', 'channel'),
            nickname=config.get('irc', 'nickname'),
            realname=config.get('irc', 'realname'),
            quotesFilename=config.get('talkback', 'quotesFilename'),
            triggers=triggers,
        )

class Options(usage.Options):
    optParameters = [
        ['config', 'c', 'settings.ini', 'Configuration file.'], 
    ]
serviceMaker = BotServiceMaker()

