#!/usr/bin/env python
"""
minimal interface to python's multiprocessing module

NOTE: pathos will refactor to multiprocessing's interface in the near future
"""
import sys
if sys.hexversion >= 0x2060000:
  import multiprocessing as mp
  from multiprocessing import cpu_count
  import multiprocessing.dummy as mpdummy
else:
  import processing as mp
  from processing import cpuCount as cpu_count
  import processing.dummy as mpdummy

__STATE = {'pool': None}


def mp_map(function, sequence, *args, **kwds):
    '''extend python's parallel map function to multiprocessing

Inputs:
    function  -- target function
    sequence  -- sequence to process in parallel

Additional Inputs:
    nproc     -- number of 'local' processors to use  [defaut = 'autodetect']
    type      -- processing type ['blocking', 'non-blocking', 'unordered']
    threads   -- if True, use threading instead of multiprocessing
    '''
    processes = cpu_count()
    proctype = 'blocking'
    threads = False
    if kwds.has_key('nproc'):
        processes = kwds['nproc']
        kwds.pop('nproc')
    if kwds.has_key('type'):
        proctype = kwds['type']
        kwds.pop('type')
    if kwds.has_key('threads'):
        threads = kwds['threads']
        kwds.pop('threads')

    # Create a new server if one isn't already initialized
    if not __STATE['pool'] or processes != cpu_count():
        if threads: __STATE['pool'] = mpdummy.Pool(processes)
        else: __STATE['pool'] = mp.Pool(processes)

    if proctype in ['blocking']:
        return __STATE['pool'].map(function,sequence,*args,**kwds)
    elif proctype in ['unordered']:
        return list(__STATE['pool'].imapUnordered(function,sequence,*args,**kwds))
    elif proctype in ['non-blocking', 'ordered']:
      return list(__STATE['pool'].imap(function,sequence,*args,**kwds))
    # default
    return __STATE['pool'].map(function,sequence,*args,**kwds)



if __name__ == '__main__':
  pass

