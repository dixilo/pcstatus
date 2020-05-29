#!/usr/bin/env python3
'''Status monitoring tool
'''
from logging import getLogger, Formatter, DEBUG, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from subprocess import CalledProcessError
from argparse import ArgumentParser

from util_remote import get_remote_status
from pcstatus import get_status
from alert import send_alert

LOGDIR = Path('.')


def do_nothing(**kwargs):
    pass


def logger_preparation(logname):
    ''' Preaparation of logger '''
    logger = getLogger(logname)
    tr_handler = TimedRotatingFileHandler(LOGDIR.joinpath(f'{logname}.log'),
                                       when='MIDNIGHT')
    tr_handler.setLevel(DEBUG)
    fmt = Formatter('[{asctime}][{levelname}]{message:s}',
                    style='{')
    tr_handler.setFormatter(fmt)
    st_handler = StreamHandler()
    st_handler.setLevel(DEBUG)

    logger.setLevel(DEBUG)
    logger.addHandler(tr_handler)
    logger.addHandler(st_handler)
    logger.propagate = False
    return logger


def check_status(hostname, cmdpath=None, logger=None, pyprocs=[], errhandler=do_nothing):
    ''' Check status of the host '''
    if logger is None:
        logger = logger_preparation(hostname)
    try:
        if hostname != 'localhost':
            status = get_remote_status(hostname, cmdpath=cmdpath)
        else:
            status = get_status()
    except CalledProcessError as err:
        logger.error(f'Remote-code excection failed: {err.returncode}')
        errhandler(message='Remote-code excection failed.',
                   hostname=hostname)
        return

    procs_dead = pyprocs.copy()
    for proc in pyprocs:
        for _, item in status['pyprocs'].items():
            if proc in ' '.join(item['cmdline']):
                procs_dead.pop(procs_dead.index(proc))
                break

    if len(procs_dead) != 0:
        logger.error(f'One or more processes dead: {procs_dead}')
        errhandler(message=f'One or more processes dead: {procs_dead}',
                   hostname=hostname)
    else:
        logger.info('OK')


def main():
    ''' Main function '''
    parser = ArgumentParser()
    parser.add_argument('hostname', type=str)
    parser.add_argument('--cmdpath', '-c', type=str, nargs='?', default=None)
    parser.add_argument('--pyprocs', '-p', type=str, nargs='*', default=[])
    args = parser.parse_args()

    check_status(args.hostname,
                 cmdpath=args.cmdpath,
                 pyprocs=args.pyprocs,
                 errhandler=send_alert)


if __name__ == '__main__':
    main()
