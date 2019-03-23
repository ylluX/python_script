#!/usr/bin/env python
import sys
import os
import re
import time
import getpass
import socket
import argparse
from commands import getstatusoutput


class Task(object):

    def __init__(self, pid):
        self.user = None
        self._pid = pid
        self.ptask = None
        self.stask = set()
        self.c = None
        self.stime = None
        self.tty = None
        self.time = None
        self.cmd = None
        self.cpu = 0
        self.mem = 0
        self.vsz = None
        self.rss = None
        self.stat = None
        self.start = None

    @property
    def pid(self):
        return self._pid


class TaskPool(object):

    tasks = []

    def __init__(self):
        pass

    def get_task(self, pid):
        for task in self.tasks:
            if task.pid == pid:
                return task
        return None

    def get_task_and_id(self, pid):
        for id, task in enumerate(self.tasks):
            if task.pid == pid:
                return id, task
        return None, None

    def add_task(self, pid):
        task = self.get_task(pid)
        if task:
            return task
        new_task = Task(pid)
        self.tasks.append(new_task)
        return new_task

    def del_task(self, pid): 
        id, task = self.get_task_and_id(pid)
        if id is not None:
            del(self.tasks[id])


class PsParser(object):

    def __init__(self):
        self.task_pool = TaskPool()

    def get_ps_result_by_cmd(self, cmd):
        status, output = getstatusoutput(cmd)
        if not status:
            return output

    def ps_ux_result_to_task(self, ps_ux_result):
        task_list = [re.split(r"\s+", i, 10) for i in ps_ux_result.split("\n")]
        return task_list[1:]

    def ps_ef_result_to_task(self, ps_ef_result):
        task_list = [re.split(r"\s+", i, 7) for i in ps_ef_result.split("\n")]
        return task_list

    def parse_ps_ux(self, task_list):
        for task in task_list:
            user, pid, cpu, mem, vsz, rss, tty, stat, start, time, command = task
            task = self.task_pool.add_task(pid)
            task.user, task.cpu, task.mem, task.vsz, task.rss, task.tty, task.stat,\
            task.start, task.time, task.command = user, cpu, mem, vsz, rss, tty,\
            stat, start, time, command

    def parse_ps_ef(self, task_list):
        for task in task_list:
            user, pid, ppid, c, stime, tty, time, cmd = task
            task = self.task_pool.add_task(pid)
            task.user, task.c, task.stime, task.tty, task.time,\
            task.cmd = user, c, stime, tty, time, cmd
            ptask  = self.task_pool.get_task(ppid)
            if not ptask:
                ptask = self.task_pool.add_task(ppid)
            task.ptask = ptask
            ptask.stask.add(task)

    def del_invalid_task(self, valid_task_pid_list):
        for task in self.task_pool.tasks:
            if task.pid not in valid_task_pid_list:
                self.task_pool.del_task(task.pid)

    def get_cpu_mem_by_pid(self, pid):
        cpu = 0
        mem = 0
        task = self.task_pool.get_task(pid)
        if task:
            for stask in task.stask:
                #print stask.pid, stask.cpu, stask.mem
                scpu, smem = self.get_cpu_mem_by_pid(stask.pid)
                cpu += scpu + float(stask.cpu)
                mem += smem + float(stask.mem)
        return cpu, mem

    def update(self):
        user = getpass.getuser()
        ux_cmd = "ps ux"
        ef_cmd = "ps -ef|grep '{}'|grep -v 'root'".format(user)
        ps_ux_result = self.get_ps_result_by_cmd(ux_cmd)
        ps_ef_result = self.get_ps_result_by_cmd(ef_cmd)
        ux_task_list = self.ps_ux_result_to_task(ps_ux_result)
        ef_task_list = self.ps_ef_result_to_task(ps_ef_result)

        task_pid_list = [i[1] for i in ux_task_list]
        self.del_invalid_task(task_pid_list)

        self.parse_ps_ux(ux_task_list)
        self.parse_ps_ef(ef_task_list)

    def get_max_cpu_mem(self, pid, steptime=10):

        print self.get_ps_result_by_cmd("ps fx") + "\n"

        max_cpu, max_mem = 0, 0
        all_mem = self.get_all_mem()
        while 1:
            self.update()
            task = self.task_pool.get_task(pid)
            if not task: break
            cpu, mem = self.get_cpu_mem_by_pid(pid)
            mem = all_mem * float(mem) / 100
            print "[{}]\tcpu(%):{}\tmem:{:2f}G".format(time.strftime("%Y-%m-%d %H:%M:%S",
                time.localtime()), cpu, mem)
            if cpu > max_cpu: max_cpu = cpu
            if mem > max_mem: max_mem = mem
            time.sleep(steptime)
        return max_cpu, max_mem

    def get_all_mem(self):
        status, output = getstatusoutput("cat /proc/meminfo|grep 'MemTotal'")
        if status:
            return None
        else:
            return float(output.split()[1]) / 1024 / 1024


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="monitor Resource By Pid")
    parser.add_argument("pid", help="pid or pid file")
    parser.add_argument("-time", help="step time to update [default:10]", type=int, default=10)
    args = parser.parse_args()

    if os.path.exists(args.pid):
        with open(args.pid, "r") as f:
            pid = f.read().strip()
    else:
        pid = args.pid

    host = socket.gethostname()
    user = getpass.getuser()

    print "HOST: {}".format(host)
    print "USER: {}".format(user)
    print "PID: {}\n".format(pid)

    pp = PsParser()
    start_time = time.time()
    max_cpu, max_mem = pp. get_max_cpu_mem(pid, steptime=args.time)
    end_time = time.time()
    run_time = int (end_time - start_time)
    print "\nALL_TIME:{}s\tMAX_CPU(%):{}\tMAX_MEM(%):{}G".format(run_time, max_cpu, max_mem)
