import re
import slack
import time
import asyncio
import concurrent.futures
from datetime import datetime


@slack.RTMClient.run_on(event='message')
async def say_hello(**payload):
    data = payload['data']
    print(data.get('text'))


def sync_loop():
    while True:
        print("Hi there: ", datetime.now())
        time.sleep(5)


async def slack_main():
    loop = asyncio.get_event_loop()
    rtm_client = slack.RTMClient(token='xoxb-761143478773-760710426068-SAL1D8gTJ0zTa1xW4rqo3Sv5', run_async=True, loop=loop)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    await asyncio.gather(
        loop.run_in_executor(executor, sync_loop),
        rtm_client.start()
    )


if __name__ == "__main__":
    asyncio.run(slack_main())
    print('edi waw')

