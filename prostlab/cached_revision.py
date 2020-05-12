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

import glob
import os.path
import subprocess

from lab.cached_revision import CachedRevision


class CachedProstRevision(CachedRevision):
    """This class represents Prost checkouts.

    It provides methods for caching and compiling given revisions.
    """

    def __init__(self, repo, rev, build_options):
        """
        * *repo*: Path to Prost repository.
        * *rev*: Prost revision.
        * *build_options*: List of build.py options.
        """
        super().__init__(repo, rev, ["./build.py"] + build_options, ["scripts"])
        self.build_options = build_options

    def _cleanup(self):
        # Strip binaries.
        binaries = []
        for path in glob.glob(os.path.join(self.path, "builds", "*", "*", "*")):
            if os.path.basename(path) in ["rddl-parser", "search"]:
                binaries.append(path)
        subprocess.call(["strip"] + binaries)

        # Compress src directory.
        subprocess.call(
            ["tar", "-cf", "src.tar", "--remove-files", "src"], cwd=self.path
        )
        subprocess.call(["xz", "src.tar"], cwd=self.path)
