#import requests
import json

from TelegramBot.helpers.functions import perform_request
from TelegramBot.helpers.odesli.entity.song.SongResult import SongResult
from TelegramBot.helpers.odesli.entity.album.AlbumResult import AlbumResult
from TelegramBot.helpers.odesli.entity.EntityResult import EntityResult

BASE_URL = 'https://api.song.link'
API_VERSION = 'v1-alpha.1'
ROOT = f'{BASE_URL}/{API_VERSION}'
LINKS_ENDPOINT = 'links'

class Odesli():
    def __init__(self, key=None):
        self.key = key

    async def __get(self, params) -> EntityResult:
        if not self.key == None:
            params['key'] = self.key
        url = f'{ROOT}/{LINKS_ENDPOINT}'
        requestResult = await perform_request(url, params)
        #await requestResult.raise_for_status()
        result = json.loads(requestResult.content.decode())
        resultType = next(iter(result['entitiesByUniqueId'].values()))['type']
        if resultType == 'song':
            return SongResult.parse(result)
        elif resultType == 'album':
            return AlbumResult.parse(result)
        else:
            raise NotImplementedError(f'Entities with type {resultType} are not supported yet.')


    async def getByUrl(self, url) -> EntityResult:
        return await self.__get({ 'url': url })

    async def getById(self, id, platform, type) -> EntityResult:
        return await self.__get({
            'id': id,
            'platform': platform,
            'type': type
        })
