#!/usr/bin/env cctbx.python

from dxtbx.model.experiment_list import ExperimentListFactory
import numpy as np

inFN = 'refined.expt'

e = ExperimentListFactory.from_json_file(inFN)
c = e[0].crystal
b = e[0].beam
g = e[0].goniometer
s = e[0].scan

A,B,C = list(c.get_real_space_vectors())


print("""
goniometer rotation axis: {}
incoming beam wavevector: {}
first image phi: {}
Real space axes at phi=0
    A axis:  {:8.3f}, {:8.3f}, {:8.3f}
    B axis:  {:8.3f}, {:8.3f}, {:8.3f}
    C axis:  {:8.3f}, {:8.3f}, {:8.3f}
""".format(g.get_rotation_axis(), b.get_s0(), s.get_oscillation()[0], *(A+B+C)))

#Rotate c in place to beginning of first wedge
phi = s.get_oscillation()[0]
c.rotate_around_origin(g.get_rotation_axis(), phi)
A,B,C = list(c.get_real_space_vectors())
print("""
Real space axes at phi={}
    A axis:  {:8.3f}, {:8.3f}, {:8.3f}
    B axis:  {:8.3f}, {:8.3f}, {:8.3f}
    C axis:  {:8.3f}, {:8.3f}, {:8.3f}
""".format(phi, *(A+B+C)))

#Rotate c in place to beginning of second wedge
phi = phi + 90.
c.rotate_around_origin(g.get_rotation_axis(), 90.)
A,B,C = list(c.get_real_space_vectors())
print("""
Real space axes at phi={}
    A axis:  {:8.3f}, {:8.3f}, {:8.3f}
    B axis:  {:8.3f}, {:8.3f}, {:8.3f}
    C axis:  {:8.3f}, {:8.3f}, {:8.3f}
""".format(phi, *(A+B+C)))
