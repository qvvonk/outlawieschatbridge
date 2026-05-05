from aiohttp import ClientSession, TCPConnector, ClientTimeout


class Translater:
    def __init__(self, api_key: str, folder_id: str):
        self._session: ClientSession | None = None
        self._connector: TCPConnector | None = None
        self._api_key = api_key
        self._folder_id = folder_id

    async def session(self):
        if self._session is None or self._session.closed:
            if self._connector is None or self._connector.closed:
                self._connector = TCPConnector()
            self._session = ClientSession(connector=self._connector, connector_owner=False)
        return self._session

    async def translate(self, text: str, to: str) -> str:
        session = await self.session()
        async with session:
            res = await session.post(
                url='https://translate.api.cloud.yandex.net/translate/v2/translate',
                json={
                    'folderId': self._folder_id,
                    'targetLanguageCode': to,
                    'texts': [text]
                },
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Api-Key {self._api_key}'
                },
                timeout=ClientTimeout(total=2.0),
            )
            json = await res.json()
            return json['translations'][0]['text']
