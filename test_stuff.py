import asyncio
import time
import functools
import asyncio.tasks
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.getLogger("asyncio").setLevel(logging.DEBUG)

class EventLoopDelayMonitor:

    def __init__(self, loop=None, start=True, interval=1, logger=None):
        self._interval = interval
        self._log = logger or logging
        self._loop = loop or asyncio.get_event_loop()
        if start:
            self.start()

    def run(self):
        self._loop.call_later(self._interval, self._handler, self._loop.time())

    def _handler(self, start_time):
        #latency = (self._loop.time() - start_time) - self._interval
        #self._log.error('EventLoop delay %.4f', latency)
        self._log.debug(self._loop.time())
        self._log.debug(asyncio.current_task(loop=self._loop))
        if not self.is_stopped():
            self.run()

    def is_stopped(self):
        return self._stopped

    def start(self):
        self._stopped = False
        self.run()

    def stop(self):
        self._stopped = True

async def foo():
    print('Running in foo')
    await asyncio.sleep(1)
    print('Explicit context switch to foo again')


async def bar():
    print('Explicit context to bar')
    await asyncio.sleep(1)
    print('Implicit context switch back to bar')


async def main():
    tasks = [foo(), bar()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.set_debug(True)  # Enable debug
    loop.slow_callback_duration = 0

    old_factory = loop.get_task_factory() or (lambda coro, loop: asyncio.tasks.Task(coro, loop=loop))

    def new_task_factory(loop, coro):
        logger.debug("Creating task: %s" % coro)
        task = old_factory(coro, loop)
        task.add_done_callback(functools.partial(logger.debug, "Completed: %s"))
        logger.debug("Created task: %s" % task)
        return task

    loop.set_task_factory(new_task_factory)
    loop.run_until_complete(main())
