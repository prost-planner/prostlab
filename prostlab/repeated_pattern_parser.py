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

"""Parse repeated patterns in logs and output files.

A repeated pattern parser extends a lab parser with the functionality to
parse a pattern that occurs repeatedly in a log or output file.

"""

import re

from lab.parser import Parser


def _get_flags(flags_string):
    flags = 0
    for char in flags_string:
        flags |= getattr(re, char)
    return flags


class RepeatedPatternParser(Parser):
    def add_repeated_pattern(self, name, regex, file="run.log", type=int, flags="M"):
        """
        *regex* must contain at most one group.
        """
        flags = _get_flags(flags)

        def find_all_occurences(content, props):
            matches = re.findall(regex, content, flags=flags)
            props[name] = [type(m) for m in matches]

        self.add_function(find_all_occurences, file=file)
