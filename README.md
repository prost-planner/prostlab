# Prost Lab

Prost Lab is a Python package for performing experiments with the [Prost
planner](https://github.com/prost-planner/prost). It is based on the
[Lab toolkit](https://github.com/aibasel/lab), so most of the [Lab
documentation](https://lab.readthedocs.io) is also relevant for Prost Lab.

## Setting up Prost Lab

To set up the virtual environment for Prost Lab in the directory
`/path/to/prostlab-venv`, perform the following steps:

 * `cd /path/to/prostlab-venv` (switch to directory)
 * `python3 -m venv prostlab-venv` (create virtual environment)
 * `source prostlab-venv/bin/activate` (activate the virtual environment)
 * `pip install -U pip` (upgrade pip)
 * `pip install prostlab` (install prostlab)

If you want to install the latest development version and/or need to
change Prost Lab itself, you can clone the Prost Lab repository and
install it in the virtual environment:

 * `git clone https://github.com/prost-planner/prostlab.git` (clone the repo)
 * `cd prostlab` (switch into prostlab directory)
 * `pip install --editable ./` (install prostlab)

In both cases, you need to define two environment variables to perform
experiments with Prost Lab:

 * PROST_BENCHMARKS points to the testbed/benchmarks directory of your prost clone
 * RDDLSIM_ROOT points to the root directory of rddlsim
 
## Performing an experiment

See [the Prost
wiki](https://github.com/prost-planner/prost/wiki/Evaluation) for
information on how to perform an experiment with Prost using Prost Lab.
