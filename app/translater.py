from aiohttp import ClientSession, TCPConnector, ClientTimeout


class Translater:
    def __init__(self, addr: str):
        self._session: ClientSession | None = None
        self._connector: TCPConnector | None = None
        self._addr = addr

    async def session(self):
        if self._session is None or self._session.closed:
            if self._connector is None or self._connector.closed:
                self._connector = TCPConnector()
            self._session = ClientSession(
                connector=self._connector, connector_owner=False, base_url=self._addr,
            )
        return self._session

    async def translate(self, text: str, orig_lang: str | None, to: str) -> str:
        session = await self.session()
        async with session:
            res = await session.post(
                url='/translate',
                json={
                    'q': text,
                    'source': orig_lang or 'auto',
                    'target': to,
                    'format': 'text',
                    'alternatives': 0
                },
                headers={
                    'Content-Type': 'application/json',
                },
                timeout=ClientTimeout(total=2.0),
            )
            r = await res.text()
            print(r)
            json = await res.json()
            return json['translatedText']
