# pipe_asyncio.py
import subprocess
import time
from asyncio import get_event_loop, wait, sleep
from asyncio import Task as AsyncioTask


class Task(AsyncioTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = len(Task.all_tasks())


async def runner(argv, timeout=0):
    argv = [str(a) for a in argv]
    cmdstr = ' '.join(argv)

    proc = subprocess.Popen(argv)
    t0 = time.time()
    print(f'Started "{cmdstr}" at t={t0}')

    while True:
        exit_code = proc.poll()
        if exit_code is None:
            # proc is still running
            if timeout and time.time() - t0 > timeout:
                # Timeout exceeded!
                proc.kill()
                raise subprocess.TimeoutExpired(cmd=cmdstr, timeout=timeout)
        else:
            # proc is done, one way or another
            return proc.returncode

        # Give other coroutines a chance to run
        await sleep(.01)


def logging_cb(task):
    t = time.time()

    if task.exception():
        print(f'Task {task.id} raised {task.exception()!r} at t={t}')
    else:
        print(
            f'Task {task.id} exited with status code {task.result()} at t={t}'
        )


if __name__ == '__main__':
    loop = get_event_loop()
    loop.set_task_factory(lambda loop, coro: Task(coro))

    tasks = [
        loop.create_task(runner(['sleep', 5])),
        loop.create_task(runner(['sleep', 10], timeout=3)),
        loop.create_task(runner(['sleep', 4])),
    ]

    for task in tasks:
        task.add_done_callback(logging_cb)

    loop.run_until_complete(wait(tasks))

# Issues
# - No stdout/stderr capturing
