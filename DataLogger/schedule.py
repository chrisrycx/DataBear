'''
A highly simplified version of the Schedule
library: https://github.com/dbader/schedule

Idea...
Create a .when method for scheduling a job based on
measurements rather than time.

'''

import datetime
import time
import functools

class Scheduler:
    """
    Copied from Schedule library, but only kept a
    subset of the functions.
    """
    def __init__(self):
        self.jobs = []

    def run_pending(self):
        """
        Run all jobs that are scheduled to run.
        Please note that it is *intended behavior that run_pending()
        does not run missed jobs*. For example, if you've registered a job
        that should run every minute and you only call run_pending()
        in one hour increments then your job won't be run 60 times in
        between but only once.
        """
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)

    def every(self, interval=1):
        """
        Schedule a new periodic job.
        :param interval: A quantity of a certain time unit
        :return: An unconfigured :class:`Job <Job>`
        """
        job = Job(interval, self)
        return job

    @property
    def next_run(self):
        """
        Datetime when the next job should run.
        :return: A :class:`~datetime.datetime` object
        """
        if not self.jobs:
            return None
        return min(self.jobs).next_run

    @property
    def idle_seconds(self):
        """
        :return: Number of seconds until
                 :meth:`next_run <Scheduler.next_run>`.
        """
        return (self.next_run - datetime.datetime.now()).total_seconds()

    def _run_job(self, job):
        ret = job.run()

class Job:
    """
    Copied from Schedule library, but eliminated most functions.
    Fixed the interval as seconds and eliminated the properties
    associated with time intervals other than seconds.
    """
    def __init__(self, interval, scheduler=None):
        self.interval = interval  # run frequency in seconds
        self.job_func = None  # the job job_func to run
        self.last_run = None  # datetime of the last run
        self.next_run = None  # datetime of the next run
        self.scheduler = scheduler  # scheduler to register with

    def __lt__(self, other):
        """
        PeriodicJobs are sortable based on the scheduled time they
        run next.
        """
        return self.next_run < other.next_run

    def _schedule_first_run(self):
        """
        Determine when first run should be.
        Start logger at top of the minute XX:00
        """
        currenttime = datetime.datetime.now()
        smin = currenttime.minute + 1
        if smin > 59:
            smin=0
        self.next_run = currenttime.replace(minute=smin,second=0,microsecond=0)

    def do(self, job_func, *args):
        """
        Specifies the job_func that should be called every time the
        job runs.
        """
        self.job_func = functools.partial(job_func, *args)
        try:
            functools.update_wrapper(self.job_func, job_func)
        except AttributeError:
            # job_funcs already wrapped by functools.partial won't have
            # __name__, __module__ or __doc__ and the update_wrapper()
            # call will fail.
            pass
        
        self._schedule_first_run()
        self.scheduler.jobs.append(self)
        return self

    @property
    def should_run(self):
        """
        :return: ``True`` if the job should be run now.
        """
        return datetime.datetime.now() >= self.next_run

    def run(self):
        """
        Run the job and immediately reschedule it.
        :return: The return value returned by the `job_func`
        """
        self.last_run = self.next_run
        ret = self.job_func()
        self.next_run = self.last_run + datetime.timedelta(seconds=self.interval)
        return ret




   
       