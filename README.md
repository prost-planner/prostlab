# Prost Lab

Prost Lab is a Python package for performing experiments with the [Prost
planner](https://github.com/prost-planner/prost). It is based on the
[Lab toolkit](https://github.com/aibasel/lab), so most of the [Lab
documentation](https://lab.readthedocs.io) is also relevant for Prost Lab.

## Setting up Prost Lab

To set up Prost Lab, perform the following steps:

 * `git clone https://github.com/prost-planner/prostlab.git /path/to/prostlab` (clone the repo)
 * `cd /path/to/prostlab` (switch to directory containing Prost Lab)
 * `python3 -m venv .venv` (create virtual environment)
 * `source .venv/bin/activate` (activate the virtual environment)
 * `pip install -U pip` (upgrade pip)
 * `pip install ./` (install prostlab)

You also need to define two environment variables to perform experiments
with Prost Lab:

 * PROST_BENCHMARKS points to the testbed/benchmarks directory of your Prost clone
 * RDDLSIM_ROOT points to the root directory of rddlsim

## Performing an experiment

See [the Prost
wiki](https://github.com/prost-planner/prost/wiki/Evaluation) for
information on how to perform an experiment with Prost using Prost Lab.
