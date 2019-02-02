import asyncio
from concurrent.futures import ProcessPoolExecutor
import time
import matplotlib.pyplot as plt
import numpy as np

async def task(loop, executor, async_sleep, sync_sleep):
    times = [time.monotonic()]
    # This is like doing some IO
    await asyncio.sleep(async_sleep)
    times.append(time.monotonic())
    # This is like doing a lot of computation
    time.sleep(sync_sleep)
    # await loop.run_in_executor(executor, time.sleep, sync_sleep)
    times.append(time.monotonic())
    return times

def visualize_runtimes(times, start_time):
    plt.cla()
    times = np.array(list(times)) - start_time
    starts = times[:,:-1]
    lengths = times[:,1:] - times[:,:-1]
    print(times)
    tasks, parts = starts.shape
    for i in range(parts):
        plt.barh(range(tasks), lengths[:,i], left=starts[:,i])
    plt.yticks([])
    plt.grid(axis='x')
    plt.ylabel("Tasks")
    plt.xlabel("Seconds")
    plt.savefig("timing.pdf")

async def run():
    start_time = time.monotonic()
    loop = asyncio.get_running_loop()
    loop.set_debug(True)
    with ProcessPoolExecutor(max_workers=4) as executor:
          times = await asyncio.gather(*[
              task(loop, executor, i, i) for i in range(1,4)])
    return times, start_time

async def main():
    visualize_runtimes(*await run())

if __name__ == "__main__":
    asyncio.run(main())
