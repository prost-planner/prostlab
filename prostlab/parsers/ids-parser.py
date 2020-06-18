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


class IDSParser(RepeatedPatternParser):
    def __init__(self):
        RepeatedPatternParser.__init__(self)

        self.add_pattern(
            "ids_learned_search_depth",
            "THTS heuristic IDS: Setting max search depth to: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "entries_det_state_value_cache",
            "Entries in deterministic state value cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "buckets_det_state_value_cache",
            "Buckets in deterministic state value cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "entries_det_applicable_actions_cache",
            "Entries in deterministic applicable actions cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "buckets_det_applicable_actions_cache",
            "Buckets in deterministic applicable actions cache: (.+)\n",
            type=int,
        )

        self.add_repeated_pattern(
            "entries_ids_reward_cache", "Entries in IDS reward cache: (.+)\n", type=int,
        )

        self.add_repeated_pattern(
            "buckets_ids_reward_cache", "Buckets in IDS reward cache: (.+)\n", type=int,
        )

        self.add_repeated_pattern(
            "ids_avg_search_depth_first_relevant_state",
            "Average search depth in first relevant state: (.+)\n",
            type=float,
        )

        self.add_repeated_pattern(
            "ids_total_num_runs", "Total number of runs: (.+)\n", type=int,
        )

        self.add_repeated_pattern(
            "ids_avg_search_depth_total",
            "Total average search depth: (.+)\n",
            type=float,
        )


def main():
    parser = IDSParser()
    parser.parse()


main()
