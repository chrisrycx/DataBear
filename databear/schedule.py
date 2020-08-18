'''
A highly simplified version of the Schedule
library: https://github.com/dbader/schedule
Copyright (c) 2013 Daniel Bader (http://dbader.org)

In addition to removing portions of the code,
a "first run" method is added to schedule that
starts logging at an even multiple of the job interval. 

Also, the next run is based on the last
scheduled run, not the last actual run in order
to keep jobs from drifting.

'''

import datetime
import time
import functools
from math import ceil

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

    def cancel_job(self, job):
        """
        Delete a scheduled job.
        :param job: The job to be unscheduled
        """
        try:
            self.jobs.remove(job)
        except ValueError:
            pass
    
    def reset(self):
        '''
        Reset schedule for all jobs
        Can be used to handle errors like clock changes
        '''
        for job in self.jobs:
            job._schedule_first_run()

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

    def __str__(self):
        return (
            "Job(interval={}, "
            "do={}, "
            "args={}, "
            "kwargs={})"
        ).format(self.interval,
                 self.job_func.__name__,
                 self.job_func.args,
                 self.job_func.keywords)

    def getsettings(self):
        '''
        Return job "settings"
        '''
        return {
            'interval':self.interval,
            'function':self.job_func.__name__,
            'args':self.job_func.args
        }

    
    def _schedule_first_run(self):
        """
        Schedule first run of job.
        Assumes preferred start time at
        the start of the next sec, min, or hr
        or some multiple of the interval.
        """
        currenttime = datetime.datetime.now()
        
        #Round everything to nearest sec
        intervalsec = ceil(self.interval)

        if intervalsec == 1:
            #If 1 or less wait til next second to start
            zerotime = currenttime.replace(
                microsecond=0)
            startsec = 1
    
        elif intervalsec <= 60:
            zerotime = currenttime.replace(
                second=0,
                microsecond=0)
            startsec = ceil(currenttime.second/intervalsec)*intervalsec

        elif intervalsec <= 3600 and intervalsec > 60:
            zerotime = currenttime.replace(
                minute=0,
                second=0,
                microsecond=0)
            secsin = currenttime.minute*60 + currenttime.second
            startsec = ceil(secsin/intervalsec)*intervalsec

        elif intervalsec <= 86400 and intervalsec > 3600:
            zerotime = currenttime.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0)
            secsin = currenttime.hour*3600 + currenttime.minute*60 + currenttime.second
            startsec = ceil(secsin/intervalsec)*intervalsec
        
        else:
            #Start immediately
            zerotime = currenttime
            startsec = 0

        self.next_run = zerotime + datetime.timedelta(seconds=startsec)

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
        #Check to see if job is on time raise error if
        #time is off
        dtdiff = datetime.datetime.now() - self.next_run
        assert abs(dtdiff.total_seconds()) < 2*self.interval
        
        #Execute job passing along current and prior runs
        #which are used by processing jobs
        ret = self.job_func(self.next_run,self.last_run)

        self.last_run = self.next_run
        self.next_run = self.last_run + datetime.timedelta(seconds=self.interval)
        return ret




   
       