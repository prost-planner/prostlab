# Prost Lab uses the Lab package to conduct experiments with the
# Prost planning system.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re

class Problem(object):
    def __init__(
        self,
        domain,
        problem,
        min_reward,
        horizon=None,
        benchmarks_dir="",
        domain_file=None,
        problem_file=None,
        max_reward=None,
        properties=dict(),
    ):
        """
        *domain* and *problem* are the display names of the domain and
        problem, and *domain_file* and *problem_file* are paths to the
        respective files on the disk.

        *min_reward* and *max_reward* are the average rewards of a minimal 
        policy and a (near-)optimal policy that are used to compute IPC scores.
        If none is provided, the minimal or maximal result of all planners is 
        used instead. 

        *properties* may be a dictionary of entries that should be added
        to the properties file of each run that uses this problem. ::

            suite = [
                Problem('elevators-2011', 1, -65.2,
                    domain_file='/path/to/elevators-2011/evelators_mdp.rddl',
                    problem_file='/path/to/elevators-2011/evelators_inst_mdp__1.rddl',
                    properties={'enums_required': False},
                Problem('elevators-2011', 1,  -65.2,
                    benchmarks_dir= '/path/to/elevators-2011/')
            ]

        """

        self.domain = domain
        self.problem = problem
        self.domain_file = domain_file
        if self.domain_file is None:
            if self.domain.endswith("-2018"):
                domain_file_name = "{}_mdp.rddl".format(self.domain[:-5])
            else:
                domain_file_name = "{}_mdp.rddl".format(self.domain[:-5].replace("-","_"))
            self.domain_file = os.path.join(benchmarks_dir, domain_file_name)
                
        self.problem_file = problem_file
        if self.problem_file is None:
            if self.domain.endswith("-2018"):
                problem_file_name = "{}_inst_mdp__{:02d}.rddl".format(self.domain[:-5], self.problem)
            else:
                problem_file_name = "{}_inst_mdp__{}.rddl".format(self.domain[:-5].replace("-","_"), self.problem)
            self.problem_file = os.path.join(benchmarks_dir, problem_file_name)

        self.problem = "inst-{:02d}".format(self.problem)
        self.problem_name = os.path.split(self.problem_file)[-1][:-5]
            
        self.min_reward = min_reward
        self.max_reward = max_reward

        self.horizon = horizon
        if self.horizon is None:
            with open(self.problem_file) as f:
                horizon_re = re.compile(r"horizon\s*=\s*(.+)\s*;\s*\n")
                for line in f:
                    match = horizon_re.search(line)
                    if match:
                        self.horizon = int(match.group(1))
                        break

        self.properties = properties

        assert(self.horizon)
        assert(os.path.exists(self.domain_file))
        assert(os.path.isfile(self.domain_file))
        assert(os.path.exists(self.problem_file))
        assert(os.path.isfile(self.problem_file))

    def __str__(self):
        return (
            "<Problem {domain}({domain_file}):{problem}({problem_file}):"
            "min_reward={min_reward}:max_reward={max_reward}:horizon={horizon}:"
            "{properties}>".format(**self.__dict__)
        )

    def __lt__(self, other):
        return str(self) < str(other)
