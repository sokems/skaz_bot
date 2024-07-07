import asyncio
from aioschedule import every, run_pending

async def job():
    print("Выполняю задачу...")

# Определите задачу, которую нужно выполнить каждые 2 секунды
every(2).seconds.do(job)

async def main():
    while True:
        await run_pending()
        await asyncio.sleep(1)

asyncio.run(main())