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


def add_planner_time(content, props):
    try:
        props["total_time"] = props["parser_time"] + props["search_time"]
    except KeyError:
        pass


class ProstParser(RepeatedPatternParser):
    def __init__(self):
        RepeatedPatternParser.__init__(self)

        self.add_pattern(
            "node", r"node: (.+)\n", type=str, file="driver.log", required=True
        )
        
        self.add_pattern(
            "planner_wall_clock_time",
            r"planner wall-clock time: (.+)s",
            type=float,
            file="driver.log",
            required=True,
        )

        self.add_pattern(
            "parser_time",
            "PROST parser complete running time: (.+)s\n",
            type=float,
        )

        self.add_pattern(
            "search_time",
            "PROST complete running time: (.+)\n",
            type=float,
        )

        self.add_function(add_planner_time)

        self.add_pattern(
            "total_reward",
            ">>> END OF SESSION  -- TOTAL REWARD: (.+)\n",
            type=float,
        )

        self.add_pattern(
            "average_reward",
            ">>> END OF SESSION  -- AVERAGE REWARD: (.+)\n",
            type=float,
        )

        self.add_repeated_pattern(
            "round_reward",
            ">>> END OF ROUND .* -- REWARD RECEIVED: (.+)\n",
            type=float,
        )


def main():
    parser = ProstParser()
    parser.parse()


main()
