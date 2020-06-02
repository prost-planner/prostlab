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

from lab.reports import Attribute, geometric_mean

from downward.reports.absolute import AbsoluteReport


class AbsoluteProstReport(AbsoluteReport):
    def __init__(self, **kwargs):
        AbsoluteReport.__init__(self, **kwargs)

        #: List of predefined :py:class:`~Attribute` instances. If
        #: PlanningReport receives ``attributes=['coverage']``, it
        #: converts the plain string ``'coverage'`` to the attribute
        #: instance ``Attribute('coverage', absolute=True,
        #: min_wins=False, scale='linear')``. Overwrites the list
        #: in PlanningReport from downward.report.

        self.PREDEFINED_ATTRIBUTES = [
            Attribute("ipc_score", min_wins=False),
            # Attributes from prost_parser
            # Attribute("node"),
            # Attribute("planner_wall_clock_time"),
            # Attribute("parser_time"),
            # Attribute("search_time"),
            # Attribute("total_time"),
            Attribute("total_reward", absolute=True, min_wins=False, function=geometric_mean),
            Attribute("average_reward", absolute=True, min_wins=False, function=geometric_mean),
            # Attribute("round_reward"),
            # Attributes from thts_parser
            # Attribute("entries_prob_state_value_cache"),
            # Attribute("buckets_prob_state_value_cache"),
            # Attribute("entries_prob_applicable_actions_cache"),
            # Attribute("buckets_prob_applicable_actions_cache"),
            # Attribute("rem_steps_first_solved_state"),
            # Attribute("trial_initial_state"),
            # Attribute("search_nodes_initial_state"),
            # Attribute("perc_exploration_initial_state"),
            # Attributes from ids_parser
            Attribute("ids_learned_search_depth", absolute=True, min_wins=False),
            # Attribute("entries_det_state_value_cache"),
            # Attribute("buckets_det_state_value_cache"),
            # Attribute("entries_det_applicable_actions_cache"),
            # Attribute("buckets_det_applicable_actions_cache"),
            # Attribute("entries_ids_reward_cache"),
            # Attribute("buckets_ids_reward_cache"),
            # Attribute("ids_avg_search_depth_initial_state"),
            # Attribute("ids_total_num_runs"),
            # Attribute("ids_avg_search_depth_total"),
        ]

        #: Attributes shown in the algorithm info table. Overwrites the
        #: list in PlanningReport from downward.report.
        self.INFO_ATTRIBUTES = [
            "local_revision",
            "global_revision",
            "revision_summary",
            "build_options",
            "parser_options",
            "driver_options",
            "search_engine",
        ]

        #: Attributes shown in the unexplained-errors table. Overwrites the
        #: list in PlanningReport from downward.report.
        self.ERROR_ATTRIBUTES = [
            "domain",
            "problem",
            "algorithm",
            "unexplained_errors",
            "planner_wall_clock_time",
            "node",
        ]
