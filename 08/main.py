""""Script for processing list of urls
using asynchronous programming """
import asyncio
import sys
import time
import argparse
import aiohttp


async def fetch(session, que):
    """Async function that gets url
    from queue and processes url """
    while True:
        url = await que.get()
        try:
            async with session.get(url) as resp:
                data = await resp.read()
                assert resp.status == 200
                print(f"{url} : {len(data)}")
        except (ValueError, TypeError):
            pass
        finally:
            que.task_done()


async def fill_queue(que, file):
    """Function that fills the queue"""
    with open(file, 'r', encoding='utf-8') as text:
        for line in text:
            await que.put(line[:-1])


async def main(work_num, file):
    """Main function that runs async workers,
    runs function that fills queue in task then
    correctly stopes worker and task"""
    que = asyncio.Queue(work_num)
    task_que = asyncio.create_task(fill_queue(que, file))
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(fetch(session, que))
            for _ in range(work_num)
        ]
        await task_que
        await que.join()

        for worker in workers:
            worker.cancel()
    stop_time = time.time()
    print(f'time: {stop_time - start_time}')


def create_parser():
    """Parses such arguments as number
    of workers and file name"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=1)
    parser.add_argument('file', type=str)
    return parser


if __name__ == '__main__':
    namespace = create_parser().parse_args(sys.argv[1:])
    w_number = namespace.c
    file_name = namespace.file
    asyncio.run(main(w_number, file_name))
