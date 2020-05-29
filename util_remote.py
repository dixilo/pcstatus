#!/usr/bin/env python3
'''Utility functions to get status of remote PCs
'''
from subprocess import check_output, CalledProcessError
from pathlib import Path

import json
import sys

def get_remote_status(hostname, cmdpath=None):
    '''Run `pcstatus.py` remotely.

    Parameters
    ----------
    host_name : str
        Host name
    cmdpath: str or None
        Path to the `pcstatus.py` in the remote machine.
        If `None`, this command sends the entire `pcstatus.py` via SSH.

    Returns
    -------
    info : dict
        Return value of `get_status` in `pcstatus.py`
    '''

    if cmdpath is None:
        path_pcs = Path(__file__).parent.joinpath('pcstatus.py')
        if not path_pcs.exists():
            raise Exception('pcstatus.py not found')
        try:
            info_raw = check_output(f'cat {str(path_pcs)} | ssh {hostname} python3',
                                    shell=True)
        except CalledProcessError as err:
            raise err
    else:
        try:
            info_raw = check_output(['ssh', hostname, cmdpath])
        except CalledProcessError as err:
            raise err

    return json.loads(info_raw)

def main():
    '''Run `get_remote_status`
    Takes the first argument to the script as the hostname
    '''
    from pprint import pprint
    pprint(get_remote_status(sys.argv[1]))

if __name__ == '__main__':
    main()
