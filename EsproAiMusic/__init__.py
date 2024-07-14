from EsproAiMusic.core.bot import EsproAi
from EsproAiMusic.core.dir import dirr
from EsproAiMusic.core.git import git
from EsproAiMusic.core.userbot import Userbot
from EsproAiMusic.misc import dbb, heroku

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
