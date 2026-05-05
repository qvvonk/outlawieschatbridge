import asyncio
from app import App


async def main():
    app = App()
    await app.start()


if __name__ == '__main__':
    asyncio.run(main())
