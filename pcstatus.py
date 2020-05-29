#!/usr/bin/env python3
'''Functions to extract status of the machine using the `psutil` module.
'''

import psutil
import getpass
import json


def get_status():
    '''Extract PC status using `psutil` module
    '''
    ret = {}
    ret['cpu_percent'] = psutil.cpu_percent()
    procs = {
                proc.pid:{
                    'cpu_percent': proc.cpu_percent(),
                    'cmdline': proc.cmdline()
                } for proc in psutil.process_iter() 
                    if ('python' in proc.name()) 
                    and (proc.username() == getpass.getuser())
            }
    ret['pyprocs'] = procs
    ret['disk_usage'] = {
        part.mountpoint:psutil.disk_usage(part.mountpoint).percent
        for part in psutil.disk_partitions() if 'rw' in part.opts
    }

    return ret


def main():
    '''Print PC status in json format
    '''
    print(json.dumps(get_status()))


if __name__ == '__main__':
    main()
