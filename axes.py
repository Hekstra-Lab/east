#!/usr/bin/env cctbx.python

from subprocess import Popen,PIPE
from argparse import ArgumentParser
from tempfile import TemporaryDirectory
from multiprocessing import cpu_count
from dxtbx.model.experiment_list import ExperimentListFactory
from os import devnull
from os.path import abspath
import numpy as np

parser = ArgumentParser()
parser.add_argument(dest="images", nargs='+', type=str, help="Image filenames")
parser.add_argument("-g", "--gain", type=float, help="Spotfinding gain setting. The default value, 1, is correct for photon counting detectors like Dectris Pilatus and Eiger.", default=1.)
parser.add_argument("-s", "--space-group", type=int, help="Space group number", required=True)
parser = parser.parse_args()

procs = cpu_count()
gain = parser.gain
spacegroup = parser.space_group
images = parser.images
images = [abspath(i) for i in images]

class DIALSError(Exception):
    """Errors from DIALS subprocess calls"""

def call_dials(command, workdir='.'):
    with open(devnull, 'w') as out:
        p = Popen(
            command,
            stdout=PIPE,
            stderr=PIPE,
            cwd=workdir,
            shell=True,
        )
        out,err = p.communicate()

    if p.returncode != 0:
        raise DIALSError(f"\nDIALSError\nNonzero exit status for {p.args[0]}\nCAPTURED ERROR MESSAGE:\n\n{err.decode()}")

with TemporaryDirectory() as workdir:
    call_dials(f"dials.import {' '.join(images)}", workdir)
    call_dials(f"dials.find_spots imported.expt spotfinder.threshold.dispersion.gain={gain} spotfinder.mp.nproc={procs}", workdir)
    call_dials(f"dials.split_experiments imported.expt strong.refl", workdir)
    call_dials('dials.combine_experiments split_* reference_from_experiment.beam=0 reference_from_experiment.goniometer=0 reference_from_experiment.detector=0', workdir)
    call_dials(f"dials.index combined.expt combined.refl space_group={spacegroup}", workdir)
    call_dials(f"dials.refine scan_varying=False indexed.expt indexed.refl", workdir)

    inFN = workdir + '/refined.expt'

    elist = ExperimentListFactory.from_json_file(inFN)

    for e in elist:
        c = e.crystal
        b = e.beam
        g = e.goniometer
        s = e.scan

        phi = s.get_oscillation()[0]
        c.rotate_around_origin(g.get_rotation_axis(), phi)
        A,B,C = list(c.get_real_space_vectors())

        first_image = e.imageset.get_image_identifier(0)    
        print("""
        Analysis of wedge starting with image: {}
        goniometer rotation axis: {}
        incoming beam wavevector: {}
        first image phi: {}
        Real space axes at phi:{}
            A axis:  {:8.3f}, {:8.3f}, {:8.3f}
            B axis:  {:8.3f}, {:8.3f}, {:8.3f}
            C axis:  {:8.3f}, {:8.3f}, {:8.3f}
        """.format(first_image, g.get_rotation_axis(), b.get_s0(), phi, phi, *(A+B+C)))

