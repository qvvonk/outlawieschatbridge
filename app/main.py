from aiogram import Bot, Dispatcher
from discord import Client, Intents
import asyncio
import os
from .routers import router as tg_router
from .translater import Translater


class App:
    def __init__(self):
        self.translater = Translater(
            folder_id=os.environ['YANDEX_FOLDER_ID'],
            api_key=os.environ['YANDEX_API_KEY']
        )
        self.tg = Bot(os.environ['TG_TOKEN'])
        self.tg_dp = Dispatcher()
        self.tg_dp.include_router(tg_router)

        self.ds_intents = Intents.default()
        self.ds_intents.message_content = True
        self.ds = Client(intents=self.ds_intents)

        self.tg_task: asyncio.Task | None = None
        self.ds_task: asyncio.Task | None = None

        self.tg_to_ds_chats = {
            (-1002373875544, None): 1499026067912917192
        }
        self.workflow_data = {
            'app': self,
            'translater': self.translater,
        }
        self.tg_dp.workflow_data = self.workflow_data

    async def start(self):
        self.tg_task = asyncio.create_task(self.tg_dp.start_polling(self.tg))
        self.ds_task = asyncio.create_task(self.ds.start(os.environ['DS_TOKEN']))
        await asyncio.wait((self.tg_task, self.ds_task), return_when=asyncio.FIRST_COMPLETED)

    @property
    def ds_to_tg_chats(self) -> dict[int, tuple[int, int | None]]:
        return {v: k for k, v in self.tg_to_ds_chats.items()}
