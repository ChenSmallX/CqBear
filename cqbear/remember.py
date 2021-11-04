# -*- coding=utf-8 -*-
"""
remember.py

  Provide an independency schedule task module which
can run by itself or in cqbear.

Expect usage::

    def foo():
        pass

    r = Remember()

    # every 30 seconds do the foo(*args, **kwargs)
    r.every(30).second.to_do(foo, *args, **kwargs)

    # every 1 minute do
    r.every().minute.to_do(foo, *args, **kwargs)

    # every 3 minute and at 20th second clock do
    r.every(3).minute.at("::24").to_do(foo, *args, **kwargs)

    # every 2 days and 8:15 clock do
    r.every(2).day.at("8:15:00").to_do(foo, *args, **kwargs)

    # every Tuesday and at 8:15 clockdo
    r.every().Tuesday.at("8:15:00").to_do(foo, *args, **kwargs)

    # every 2 month at 5th's 8:15 clock do
    r.every(2).month_day(5).at("8:15:00").to_do(foo, *args, **kwargs)

    r.parallel_run()  # or r.padding_run
"""

import time
import calendar
import datetime
import threading
import functools
from typing import Callable, List, Optional


class RememberException(Exception):
    pass


class Remember:
    """A schedule job runner for CqBear which can run without CqBear

    RECOMMEND USAGE
    ---
    - simple sumery::

        def foo(args):
            pass

        remember = Remember(job_interval=0.5)
        remember.every(2).second.to_do(foo, args)
        remember.parallel_run()  # or use remember.padding_run

    - generate a `cqbear.remember.Job` object::

        remember.every() -> Job

    - add job manually::

        remember.add_job(Job()...)

    - run the all binded jobs

        1. run on one by one mode
        2. run all job at same time(depends on multi-thread)::

            remember.padding_run()
            remember.parallel_run()

    - get the running status::

        remember.is_running -> bool

    - stop running job queue::

        remember.pause()
    """
    def __init__(self, job_interval: float = 0.5):
        """- job__interval: second(float)"""
        self.__jobs: List[Job] = []
        self.__job_thread: List[threading.Thread] = []

        self.__interval = job_interval  # interval (second)
        self.__running = False
        self.__run_end = False

    def every(self, interval: int = 1):
        """create a job for the remember and return it for configuring"""
        job = Job(self, interval)
        self.__jobs.append(job)
        return job

    def add_job(self, job):
        """add job into job list"""
        assert isinstance(job, Job)
        if job not in self.__jobs:
            self.__jobs.append(job)

    def padding_run(self, interval: float = None):
        """execute the job if the job is time to run *one by one*.

        - another run method: `parallel_run`
        """
        if self.__running:
            raise RememberException(f"Remember<{self}> is already running")

        self.__run_end = False
        self.__running = True
        try:
            while True:
                # padding run mode not need interval specially
                if interval:
                    time.sleep(interval)
                elif self.__interval:
                    time.sleep(self.__interval)

                for job in self.__jobs:
                    if self.__run_end:
                        break
                    if job.is_time_to_run():
                        job.run()
                if self.__run_end:
                    break
        finally:
            self.__running = False

    def __clean_job_thread(self):
        remove_job_thread = []
        for thread in self.__job_thread:
            if not thread.is_alive():
                remove_job_thread.append(thread)
        for thread in remove_job_thread:
            self.__job_thread.remove(thread)

    def parallel_run(self):
        """execute the job if the job is time to run *at the same time*.

        - another run method: `padding_run`
        """
        if self.__running:
            raise RememberException(f"Remember<{self}> is already running")

        self.__run_end = False
        self.__running = True
        try:
            while True:
                time.sleep(self.__interval if self.__interval else 0.5)
                for job in self.__jobs:
                    if self.__run_end:
                        break

                    if not job.is_time_to_run():
                        continue
                    t = threading.Thread(target=job.run)
                    self.__job_thread.append(t)
                    t.run()

                if self.__run_end:
                    for thread in self.__job_thread:
                        thread.join()
                    self.__clean_job_thread()
                    break
                else:
                    self.__clean_job_thread()
        finally:
            self.__running = False

    @property
    def is_running(self):
        return self.__running

    def pause(self):
        self.__run_end = True


class Job:
    """the Job element class for cqbear.remember.Remember

    ORIGIN USAGE:
    ---
    - sumery::

        job = Job().every(2).hour.at(":30:24").to_do(foo, **{params=values})

        Job().every(2).hour.at(":30:24").to_do(foo, **{params=values})\
.bind_remember(r)

        job_deco = Job().every(5).second
        @job_deco.deco(r, *args, **kwargs)
        def foo():
            pass

    - set interval number of unit::

        job = Job(interval=6)
        job = Job().every(6)

    - set interval time unit

        . clock unit::

            job.second
            job.minute
            job.hour

        . weekday unit::

            job.Monday
            job.Tuesday
            job.Wednesday
            job.Thursday
            job.Friday
            job.Saturday
            job.Sunday
            job.week(0) [NOT RECOMMAND]

        . month day unit::

            job.month_day(5)

    RECOMMAND USAGE:
    ---
    - create Job object by `cqbear.remember.Remember.every()`
    - execute by `cqbear.remember.Remember.parallel_run()` \
        or `cqbear.remember.Remember.padding_run()`
    """
    def __init__(self, remember=None, interval=1):
        self.__remember = remember
        self.__interval = interval
        self.__unit = None
        self.__weekday = None
        self.__monthday = None
        self.__at: Optional[datetime.time] = None
        self.__func: Optional[Callable] = None

        self.__last_run = None
        self.__next_run = None

        self.__is_init: bool = False

    def __repr__(self) -> str:
        classname = __class__
        func_str = self.__func.__name__ if self.__func else "no func"
        time_str = str(self.__next_run).strip("datetime.time") if \
            self.__next_run else "not set time or not called initialize()"
        return f"<{classname}>: [{func_str}] (next run at {time_str})"

    def __str__(self) -> str:
        return self.__repr__()

    def every(self, interval=1):
        """set run interval number of unit(set unit by second/minute etc...)"""
        self.__interval = interval
        return self

    def to_do(self, func: Callable, *args, **kwargs):
        self.__func = functools.partial(func, *args, **kwargs)
        try:
            functools.update_wrapper(self.__func, func)
        except AttributeError:
            pass
        return self

    @property
    def runable(self):
        return True if self.__func else False

    def run(self):
        if not self.runable:
            raise RememberException(
                f"{self} call run method must set a callable object by to_do")
        if not self.__is_init:
            self.initialize()
        if self.is_time_to_run():
            self.__update_run_time()
            return self.__func()

    def is_time_to_run(self) -> bool:
        if not self.__is_init:
            self.initialize()
        return self.__next_run < datetime.datetime.now()

    @property
    def second(self):
        """set run interval unit by second"""
        self.__unit = "seconds"
        return self

    @property
    def minute(self):
        """set run interval unit by minute"""
        self.__unit = "minutes"
        return self

    @property
    def hour(self):
        """set run interval unit by hour"""
        self.__unit = "hours"
        return self

    @property
    def day(self):
        """set run interval unit by day"""
        self.__unit = "days"
        return self

    def week(self, week_day: int):
        """set run interval unit by week

        - param weekday:

            `import calendar`\n
            Job.week(`calendar.SUNDAY`)

        RECOMMAND:
        - use weekday name to set week unit suck as `Job.Sunday` and \
            `Job.Monday` and `...`"""
        assert calendar.MONDAY <= week_day <= calendar.SUNDAY

        self.__unit = "weeks"
        self.__weekday = week_day
        return self

    @property
    def Sunday(self):
        """set run interval unit to every Sunday"""
        self.week(calendar.SUNDAY)
        return self

    @property
    def Monday(self):
        """set run interval unit to every Monday"""
        self.week(calendar.MONDAY)
        return self

    @property
    def Tuesday(self):
        """set run interval unit to every Tuesday"""
        self.week(calendar.TUESDAY)
        return self

    @property
    def Wednesday(self):
        """set run interval unit to every Wednesday"""
        self.week(calendar.WEDNESDAY)
        return self

    @property
    def Thursday(self):
        """set run interval unit to every Thursday"""
        self.week(calendar.THURSDAY)
        return self

    @property
    def Friday(self):
        """set run interval unit to every Friday"""
        self.week(calendar.FRIDAY)
        return self

    @property
    def Saturday(self):
        """set run interval unit to every Saturday"""
        self.week(calendar.SATURDAY)
        return self

    def month_day(self, day: int):
        """set run interval unit by month

        - param day: must between `1` and `31`"""
        assert 1 <= day <= 31

        self.__unit = "month"
        self.__monthday = day
        return self

    def at(self, time_str: str):
        """
        recommand time string format
        ---
        h:m:s

        support format:
        ---
        3 time parts:

        ` 12:6:4`  : 12 o'clock 6 min 4 second\n
        ` :6:4`    : 0  o'clock 6 min 4 second\n
        ` ::4`     : 0  o'clock 0 min 4 second\n

        2 time parts:

        ` 12:6`    : 12 o'clock 6 min 0 second\n
        ` :6`      : 0  o'clock 6 min 0 second\n

        1 time part:

        ` 12`      : 12 o'clock 0 min 0 second\n

        """
        time_lst = [
            int(split) if split else 0
            for split in time_str.split(":")
        ]
        hour = time_lst[0] if len(time_lst) >= 1 else 0
        minute = time_lst[1] if len(time_lst) >= 2 else 0
        second = time_lst[2] if len(time_lst) >= 3 else 0

        self.__at = datetime.time(hour=hour, minute=minute, second=second)
        return self

    def initialize(self):
        if self.__is_init:
            return self.__update_run_time()

        next_run = datetime.datetime.now().replace(microsecond=0)
        # if the default time of every day is 0:0:0
        # next_run = datetime.datetime.now().replace(
        #     second=0,
        #     minute=0,
        #     hour=0)
        if not self.__at:
            if self.__unit == "weeks":
                while next_run.weekday() != self.__weekday:
                    next_run += datetime.timedelta(days=1)
            elif self.__unit == "month":
                while next_run.day != self.__monthday:
                    next_run += datetime.timedelta(days=1)
        else:
            if self.__unit == "seconds":
                ...
            elif self.__unit == "minutes":
                next_run = next_run.replace(second=self.__at.second)
            elif self.__unit == "hours":
                next_run = next_run.replace(second=self.__at.second,
                                            minute=self.__at.minute)
            elif self.__unit == "days":
                next_run = next_run.replace(second=self.__at.second,
                                            minute=self.__at.minute,
                                            hour=self.__at.hour)
            else:
                next_run = next_run.replace(second=self.__at.second,
                                            minute=self.__at.minute,
                                            hour=self.__at.hour)
                if self.__unit == "weeks":
                    while next_run.weekday() != self.__weekday:
                        next_run += datetime.timedelta(days=1)
                elif self.__unit == "month":
                    while next_run.day != self.__monthday:
                        next_run += datetime.timedelta(days=1)

        while next_run < datetime.datetime.now():
            next_run = self.__calculate_next(next_run)
        self.__next_run = next_run
        self.__is_init = True

    def __update_run_time(self):
        self.__last_run = self.__next_run
        while self.__next_run < datetime.datetime.now():
            self.__next_run = self.__calculate_next(self.__last_run)

    def __calculate_next(self, next_run: datetime.datetime):
        if self.__unit != "month":
            next_run = next_run + datetime.timedelta(
                **{self.__unit: self.__interval})
        else:
            if next_run.month != 12:
                next_run = next_run.replace(month=(next_run.month+1))
            else:
                # the next run time of Dec is Jan of next year
                next_run = next_run.replace(
                    month=(next_run.month+1),
                    year=(next_run.year+1)
                )
        return next_run

    def bind_remember(self, remember: Remember):
        remember.add_job(self)
        return self

    def deco(self, remember: Remember, *args, **kwargs):
        def wrapper(func):
            self.to_do(func, *args, **kwargs)
            remember.add_job(self)
            return func
        return wrapper


def every(interval=1):
    """create a job for the remember and return it for configuring

    Return:
        Job object which not bind remember
    """
    return Job(remember=None, interval=1)


if __name__ == "__main__":
    import datetime

    def test(i: int):
        print(f"in test_{i}: now is {datetime.datetime.now()}")

    now = datetime.datetime.now()
    print(f"now is {datetime.datetime.now()}")

    r = Remember()
    r.every(1).minute.at("::20").to_do(test, 1)
    r.every(2).minute.at("::30").to_do(test, 2)
    r.every(1).Monday.at("18:30:20").to_do(test, 3)
    r.every(2).month_day(1).at("18:30:30").to_do(test, 4)
    r.every().month_day(5).at("18:30:30").to_do(test, 5)
    r.every(1).minute.at("::20").to_do(test, 6)

    Job().every(1).minute.at("::15").bind_remember(r).to_do(test, 7)
    job_by_deco = Job().every(5).second

    @job_by_deco.deco(r, 20)
    def foo(x):
        print(f"in test_{x}: now is {datetime.datetime.now()}")

    print("in main: running...")
    r.parallel_run()
