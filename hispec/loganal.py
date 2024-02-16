#!/usr/bin/env python
"""Analyze camerad log files"""
import sys
import datetime
import numpy as np

ofile = sys.argv[1].split('.')[0] + '.dat'
ofn = open(ofile, 'w')

tfmt = "%Y-%m-%dT%H:%M:%S.%f"
nexp = 0
nseq = -1
seqno = 1
in_exposure = False
print("")
with open(sys.argv[1]) as fn:
    lines = fn.readlines()
    for ln in lines:
        ts_str = ln.split()[0]

        if " hroi " in ln:
            # print(ln)
            vstart = int(ln.split()[-4])
            vstop = int(ln.split()[-3])
            hstart = int(ln.split()[-2])
            hstop = int(ln.split()[-1])

        if "FASTLOADPARAM Expose " in ln:
            # print(ln)
            nseq = int(ln.split()[-1])
            nexp = 0
            deltas = []

        if "waiting for new frame:" in ln:
            # print(ln)
            ts_exp_start = datetime.datetime.strptime(ts_str, tfmt)
            in_exposure = True

        if "READOUT COMPLETE" in ln:
            # print(ln)
            if in_exposure:
                ts_exp_stop = datetime.datetime.strptime(ts_str, tfmt)
                deltas.append(ts_exp_stop - ts_exp_start)
                nexp += 1
                in_exposure = False
            elif nexp > 1:
                print("Sequence %d" % seqno)
                print(vstart, vstop, hstart, hstop)
                print(vstop-vstart+1, "x", hstop-hstart+1)
                print(nexp, "out of ", nseq)
                gdelts = deltas[1:]
                d_hz = []
                for d in gdelts:
                    d_hz.append(1.e6/d.microseconds)
                d_hz = np.asarray(d_hz)
                print("Hz = %.3f +- %.3f" % (d_hz.mean(), d_hz.std()))
                print("")
                ofn.write(
                    "%3d %4d %4d %4d %4d %3d %3d %3d %3d %8.3f %8.3f\n"
                    % (seqno, vstart, vstop, hstart, hstop,
                       vstop-vstart+1, hstop-hstart+1, nexp, nseq,
                       d_hz.mean(), d_hz.std()))
                seqno += 1
            else:
                print("Sequence %d" % seqno)
                print(vstart, vstop, hstart, hstop)
                print(vstop - vstart + 1, "x", hstop - hstart + 1)
                print(nexp, "out of ", nseq)
                print("")
                seqno += 1

ofn.close()
