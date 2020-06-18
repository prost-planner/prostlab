#! /usr/bin/env python
#
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

from prostlab.repeated_pattern_parser import RepeatedPatternParser


class THTSParser(RepeatedPatternParser):
    def __init__(self):
        RepeatedPatternParser.__init__(self)

        self.add_repeated_pattern(
            "entries_prob_state_value_cache",
            "Entries in probabilistic state value cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "buckets_prob_state_value_cache",
            "Buckets in probabilistic state value cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "entries_prob_applicable_actions_cache",
            "Entries in probabilistic applicable actions cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "buckets_prob_applicable_actions_cache",
            "Buckets in probabilistic applicable actions cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "rem_steps_first_solved_state",
            "Number of remaining steps in first solved state: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "trials_first_relevant_state",
            "Number of trials in first relevant state: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "search_nodes_first_relevant_state",
            "Number of search nodes in first relevant state: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "perc_exploration_first_relevant_state",
            "Percentage exploration in first relevant state: (.+)\n",
            type=float,
        )


def main():
    parser = THTSParser()
    parser.parse()


main()
