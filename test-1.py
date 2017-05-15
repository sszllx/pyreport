
import asyncio
# import time


@asyncio.coroutine
def hello(url):
    print(url)

loop = asyncio.get_event_loop()

tasks = []
# I'm using test server localhost, but you can use any url
url = "http://localhost:8080/{}"
for i in range(5):
    print("1111111111")
    task = asyncio.ensure_future(hello(url.format(i)))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
print(len(tasks))
