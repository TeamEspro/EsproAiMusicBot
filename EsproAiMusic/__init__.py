from EsproMusicBot.core.bot import EsproAi
from EsproMusicBot.core.dir import dirr
from EsproMusicBot.core.git import git
from EsproMusicBot.core.userbot import Userbot
from EsproMusicBot.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = EsproAi()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
