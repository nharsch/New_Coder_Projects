from ConfigParser import ConfigParser

from twisted.application.service import IServiceMaker, Service
from twisted.internet.endpoints import clientFromString
from twisted.plugin import IPlugin
from twisted.python import usage, log
from zope.interface import implementer

from talkback.bot import TalkBackBotFactory
from talkback.quote_picker import QuotePicker

class TalkBackBotService(Service):
    '''create the talkback service'''

    def __init__(self, endpoint, channel, nickname, realname, 
                 quotesFilename, triggers):
        self._endpoint = endpoint
        self._channel = channel
        self._nickname = nickname
        self._realname = nickname
        self._realname = realname
        self._quotesFilename = quotesFilename
        self._triggers = triggers

    def startService(self):
        """Contruct a client & connect to server."""
        # need to import reactor now do that we don't use default reactor 
        # implementation
        from twisted.internet import reactor

        def connected(bot):
            self._bot = bot

        def failure(err):
            log.err(err, _why="Could not connect to specified server.")
            rector.stop()

        quotes = QuotePicker(self._quotesFilename)
        # instatiate client to enpoint defined in ini
        client = clientFromString(reactor, self._endpoint)
        # create factory with our settings
        factory = TalkBackBotFactory(
            self._channel,
            self._nickname,
            self._realname,
            quotes,
            self._triggers,
        )
        # connect to client with factory
        return client.connect(factory).addCallbacks(connected, failure)

    def stopService(self):
        """Disconnect."""
        if self._bot and self._bot.transport.connected:
            self._bot.transport.loseConnection()

class Options(usage.Options):
    optParameters = [
        ['config', 'c', 'settings.ini', 'Configuration file.'], 
    ]

@implementer(IServiceMaker, IPlugin)
class BotServiceMaker(object):
    tapname = "twsrs" # short name for our plugin
    description = "IRC bot that provides quotations from notable women"
    options = Options


    def makeService(self, options):
        """Construct the talkbackbot service."""
        config = ConfigParser()
        config.read([options['config']]) # read from options
        # find all the triggers in the ini file
        triggers = [
            # strip each trigger
            trigger.strip()
            # for every line
            for trigger in config.get('talkback', 'triggers').split('\n') 
            # if there's anything in that line
            if trigger.strip()
        ]
        # instantiate service
        return TalkBackBotService(
            endpoint=config.get('irc', 'endpoint'), 
            channel=config.get('irc', 'channel'),
            nickname=config.get('irc', 'nickname'),
            realname=config.get('irc', 'realname'),
            quotesFilename=config.get('talkback', 'quotesFilename'),
            triggers=triggers,
        )


serviceMaker = BotServiceMaker()

