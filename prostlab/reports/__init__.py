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

"""
Module that permits generating Prost reports by reading properties files.
"""

from collections import defaultdict
from fnmatch import fnmatch
import logging

from lab import tools
from lab.reports import arithmetic_mean, Attribute, CellFormatter, geometric_mean, markup, Report, Table


def elementwise_func(cells, func):
    len_list = max([len(cell) for cell in cells])
    result = []
    for index in range(0,len_list):
        values = [cell[index] for cell in cells if index < len(cell) and cell[index] is not None]
        if values:
            result.append(func(values))
        else:
            result.append(None)
    return result

def elementwise_arithmetic_mean(cells):
    return elementwise_func(cells, arithmetic_mean)

def elementwise_geometric_mean(cells):
    return elementwise_func(cells, geometric_mean)

def elementwise_sum(cells):
    return elementwise_func(cells, sum)

def elementwise_max(cells):
    return elementwise_func(cells, max)

def elementwise_min(cells):
    return elementwise_func(cells, min)

def rgb_fractions_to_html_colors(colors):
    if isinstance(colors, list):
        res = []
        for color in colors:
            res.append(tools.rgb_fractions_to_html_color(*color))
        return res
    return tools.rgb_fractions_to_html_color(*colors)

    
def get_elementwise_colors(cells, min_wins):
    """Returns element-wise colors over all lists of values in *cells*.
    """
    contains_list = any(isinstance(cell, list) for cell in cells.values())
    if not contains_list:
        return tools.get_colors(cells, min_wins)

    num_elements = max([len(cell) for cell in cells.values()])
    res = {key : [] for key in cells}

    for index in range(num_elements):
        values = {key : cell[index] if index < len(cell) else None for key, cell in cells.items()}
        colors = tools.get_colors(values, min_wins)
        for key, color in colors.items():
            res[key].append(color)
    return res

def get_elementwise_min_max(items):
    """Returns element-wise min and max over all lists of values in *items*.

    The length of the output is equal to the longest list in the input.
    """
    contains_lists = all(isinstance(item, list) for item in items)
    if not contains_lists:
        return (tools.get_min_max(items))

    num_elements = max([len(item) for item in items])
    res = []

    for index in range(num_elements):
        values = [item[index] if index < len(item) else None for item in items]
        res.append((tools.get_min_max(values)))
    return res


class PlanningReport(Report):
    """
    This is the base class for Prost planner reports.

    The :py:attr:`~INFO_ATTRIBUTES` and :py:attr:`~ERROR_ATTRIBUTES`
    class members hold attributes for Fast Downward experiments by
    default. You may want to adjust the two lists in derived classes.

    """

    #: List of predefined :py:class:`~Attribute` instances. If
    #: PlanningReport receives ``attributes=['coverage']``, it converts
    #: the plain string ``'coverage'`` to the attribute instance
    #: ``Attribute('coverage', absolute=True, min_wins=False, scale='linear')``.
    #: The list can be overriden in subclasses.
    PREDEFINED_ATTRIBUTES = [
        Attribute("ipc_score", absolute=True, min_wins=False),
        
        # Attributes from prost_parser
        Attribute("total_time", function=geometric_mean),
        Attribute("total_reward", min_wins=False),
        Attribute("average_reward", min_wins=False),
        Attribute("round_reward", min_wins=False, function=elementwise_sum),
        
        # Attributes from thts_parser
        Attribute("entries_prob_state_value_cache", function=elementwise_max),
        Attribute("buckets_prob_state_value_cache", function=elementwise_max),
        Attribute("entries_prob_applicable_actions_cache", function=elementwise_max),
        Attribute("buckets_prob_applicable_actions_cache", function=elementwise_max),
        Attribute("rem_steps_first_solved_state", function=elementwise_arithmetic_mean, min_wins=False),
        Attribute("trials_first_relevant_state", function=elementwise_geometric_mean, min_wins=False),
        Attribute("search_nodes_first_relevant_state", function=elementwise_geometric_mean, min_wins=False),
        Attribute("perc_exploration_first_relevant_state", function=elementwise_sum),
        
        # Attributes from ids_parser
        Attribute("ids_learned_search_depth", min_wins=False),
        Attribute("entries_det_state_value_cache", function=elementwise_max),
        Attribute("buckets_det_state_value_cache", function=elementwise_max),
        Attribute("entries_det_applicable_actions_cache", function=elementwise_max),
        Attribute("buckets_det_applicable_actions_cache", function=elementwise_max),
        Attribute("entries_ids_reward_cache", function=elementwise_max),
        Attribute("buckets_ids_reward_cache", function=elementwise_max),
        Attribute("ids_avg_search_depth_first_relevant_state", function=elementwise_sum, min_wins=False),
        Attribute("ids_total_num_runs", function=elementwise_sum, min_wins=False),
        Attribute("ids_avg_search_depth_total", function=elementwise_sum, min_wins=False),
    ]

    #: Attributes shown in the algorithm info table. Can be overriden in
    #: subclasses.
    INFO_ATTRIBUTES = [
        "local_revision",
        "global_revision",
        "revision_summary",
        "build_options",
        "parser_options",
        "driver_options",
        "search_engine",
    ]

    #: Attributes shown in the unexplained-errors table. Can be overriden
    #: in subclasses.
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "planner_wall_clock_time",
        "raw_memory",
        "node",
    ]

    ERROR_LOG_MAX_LINES = 100

    def __init__(self, **kwargs):
        """
        See :class:`~lab.reports.Report` for inherited parameters.

        You can filter and modify runs for a report with
        :py:class:`filters <.Report>`. For example, you can include only
        a subset of algorithms or compute new attributes. If you provide
        a list for *filter_algorithm*, it will be used to determine the
        order of algorithms in the report.

        >>> # Use a filter function to select algorithms.
        >>> def only_prost2011_and_prost2014(run):
        ...     return run['algorithm'] in ['prost2011', 'prost2014']
        >>> report = PlanningReport(filter=only_prost2011_and_prost2014)

        >>> # Use "filter_algorithm" to select and *order* algorithms.
        >>> r = PlanningReport(filter_algorithm=['prost2014', 'prost2011'])

        :py:class:`Filters <.Report>` can be very helpful so we
        recommend reading up on them to use their full potential.

        """
        # Set non-default options for some attributes.
        attributes = tools.make_list(kwargs.get("attributes"))
        kwargs["attributes"] = [self._prepare_attribute(attr) for attr in attributes]

        # Remember the order of algorithms if it is given as a keyword argument filter.
        self.filter_algorithm = tools.make_list(kwargs.get("filter_algorithm"))

        super().__init__(**kwargs)

    def _prepare_attribute(self, attr):
        predefined = {str(attr): attr for attr in self.PREDEFINED_ATTRIBUTES}
        if not isinstance(attr, Attribute):
            if attr in predefined:
                return predefined[attr]
            for pattern in predefined.values():
                if fnmatch(attr, pattern):
                    return pattern.copy(attr)
        return super()._prepare_attribute(attr)

    def _apply_filter(self):
        super()._apply_filter()
        if "ipc_score" in self.attributes:
            self._compute_ipc_scores()

    def _compute_ipc_scores(self):
        max_rewards = dict()
        for run in self.props.values():
            if run["max_reward"] is None and "average_reward" in run:
                reward = run["average_reward"]
                domain_name = run["domain"]
                problem_name = run["problem"]
                if (domain_name, problem_name) not in max_rewards:
                    max_rewards[(domain_name, problem_name)] = reward
                else:
                    max_rewards[(domain_name, problem_name)] = max(max_rewards[(domain_name, problem_name)], reward)
        for run in self.props.values():
            domain_name = run["domain"]
            problem_name = run["problem"]
            if (domain_name, problem_name) in max_rewards:
                run["max_reward"] = max_rewards[(domain_name, problem_name)]

            if "average_reward" not in run:
                run["ipc_score"] = 0.0
                continue
            avg_reward = run["average_reward"]
            min_reward = run["min_reward"]
            max_reward = run["max_reward"]
            dist = avg_reward - min_reward
            if dist > 0.0:
                span = max_reward - min_reward
                assert span > 0.0
                run["ipc_score"] =  dist / span
            else:
                run["ipc_score"] = 0.0

    def _scan_data(self):
        self._scan_planning_data()
        super()._scan_data()

    def _scan_planning_data(self):
        problems = set()
        self.domains = defaultdict(list)
        self.problem_runs = defaultdict(list)
        self.domain_algorithm_runs = defaultdict(list)
        self.runs = {}
        for run in self.props.values():
            domain, problem, algo = run["domain"], run["problem"], run["algorithm"]
            problems.add((domain, problem))
            self.problem_runs[(domain, problem)].append(run)
            self.domain_algorithm_runs[(domain, algo)].append(run)
            self.runs[(domain, problem, algo)] = run
        for domain, problem in problems:
            self.domains[domain].append(problem)

        self.algorithms = self._get_algorithm_order()

        num_unexplained_errors = sum(
            int(bool(tools.get_unexplained_errors_message(run)))
            for run in self.runs.values()
        )
        func = logging.info if num_unexplained_errors == 0 else logging.error
        func(
            "Report contains {num_unexplained_errors} runs with unexplained"
            " errors.".format(**locals())
        )

        if len(problems) * len(self.algorithms) != len(self.runs):
            logging.warning(
                f"Not every algorithm has been run on every task. "
                f"However, if you applied a filter this is to be "
                f"expected. If not, there might be old properties in the "
                f"eval-dir that got included in the report. "
                f"Algorithms ({len(self.algorithms)}): {self.algorithms},"
                f"problems ({len(problems)}), domains ({len(self.domains)}): "
                f"{list(self.domains.keys())}, runs ({len(self.runs)})"
            )

        # Sort each entry in problem_runs by algorithm.
        algo_to_index = {
            algorithm: index for index, algorithm in enumerate(self.algorithms)
        }

        def run_key(run):
            return algo_to_index[run["algorithm"]]

        for problem_runs in self.problem_runs.values():
            problem_runs.sort(key=run_key)

        self.algorithm_info = self._scan_algorithm_info()

    def _scan_algorithm_info(self):
        info = {}
        for runs in self.problem_runs.values():
            for run in runs:
                info[run["algorithm"]] = {
                    attr: run.get(attr, "?") for attr in self.INFO_ATTRIBUTES
                }
            # We only need to scan the algorithms for one task.
            break
        return info

    def _get_node_names(self):
        return {
            run.get("node", "<attribute 'node' missing>") for run in self.runs.values()
        }

    def _format_unexplained_errors(self, errors):
        """
        Preserve line breaks and white space. If text has more than
        ERROR_LOG_MAX_LINES lines, omit lines in the middle of the text.
        """
        linebreak = "\\\\"
        text = f"''{errors}''".replace("\\n", linebreak).replace(
            " ", markup.ESCAPE_WHITESPACE
        )
        lines = text.split(linebreak)
        if len(lines) <= self.ERROR_LOG_MAX_LINES:
            return text
        index = (self.ERROR_LOG_MAX_LINES - 2) // 2
        text = linebreak.join(lines[:index] + ["", "[...]", ""] + lines[-index:])
        assert text.startswith("''") and text.endswith("''"), text
        return text

    def _get_warnings_text_and_table(self):
        """
        Return a :py:class:`Table <lab.reports.Table>` containing one line for
        each run where an unexplained error occured.
        """
        if not self.ERROR_ATTRIBUTES:
            logging.critical("The list of error attributes must not be empty.")

        table = Table(title="Unexplained errors")
        table.set_column_order(self.ERROR_ATTRIBUTES)

        wrote_to_slurm_err = any(
            "output-to-slurm.err" in run.get("unexplained_errors", [])
            for run in self.runs.values()
        )

        for run in self.runs.values():
            error_message = tools.get_unexplained_errors_message(run)
            if error_message:
                logging.error(error_message)
                run_dir = run["run_dir"]
                for attr in self.ERROR_ATTRIBUTES:
                    value = run.get(attr, "?")
                    if attr == "unexplained_errors":
                        value = self._format_unexplained_errors(value)
                        # Use formatted value as-is.
                        table.cell_formatters[run_dir][attr] = CellFormatter()
                    table.add_cell(run_dir, attr, value)

        errors = []

        if wrote_to_slurm_err:
            src_dir = self.eval_dir.rstrip("/")[: -len("-eval")]
            slurm_err_file = src_dir + "-grid-steps/slurm.err"
            try:
                slurm_err_content = tools.get_slurm_err_content(src_dir)
            except OSError:
                slurm_err_content = (
                    "The slurm.err file was missing while creating the report."
                )
            else:
                slurm_err_content = tools.filter_slurm_err_content(slurm_err_content)

            logging.error("There was output to {slurm_err_file}.".format(**locals()))

            errors.append(
                ' Contents of {slurm_err_file} without "memory cg"'
                " errors:\n```\n{slurm_err_content}\n```".format(**locals())
            )

        if table:
            errors.append(str(table))

        infai_1_nodes = {f"ase{i:02d}.cluster.bc2.ch" for i in range(1, 25)}
        infai_2_nodes = {f"ase{i:02d}.cluster.bc2.ch" for i in range(31, 55)}
        nodes = self._get_node_names()
        if nodes & infai_1_nodes and nodes & infai_2_nodes:
            errors.append("Report combines runs from infai_1 and infai_2 partitions.")

        return "\n".join(errors)

    def _get_algorithm_order(self):
        """
        Return a list of algorithms in the order determined by the user.

        If 'filter_algorithm' is given, algorithms are sorted in that
        order. Otherwise, they are sorted alphabetically.

        You can use the order of algorithms in your own custom report
        subclasses by accessing self.algorithms which is calculated in
        self._scan_planning_data.

        """
        all_algos = {run["algorithm"] for run in self.props.values()}
        if self.filter_algorithm:
            # Other filters may have changed the set of available algorithms by either
            # removing all runs for one algorithm or changing run['algorithm'] for a run.
            # Maintain the original order of algorithms and only keep algorithms that
            # still have runs after filtering. Then add all new algorithms
            # sorted naturally at the end.
            algo_order = [
                c for c in self.filter_algorithm if c in all_algos
            ] + tools.natural_sort(all_algos - set(self.filter_algorithm))
        else:
            algo_order = tools.natural_sort(all_algos)
        return algo_order

    
class ProstTable(Table):
    """
    This is a specialized Table class for Prost reports that supports element-wise 
    coloring and aggregation of lists.
    """

    def __init__(self, title="", min_wins=None, colored=False, digits=2):
        super().__init__(title, min_wins, colored, digits)

    def _format_row(self, row_name, row):
        """Format all entries in **row** (in place)."""
        if row_name == self.header_row:
            for col_name, value in row.items():
                # Allow breaking after underlines.
                value = value.replace("_", "_" + markup.ESCAPE_WORDBREAK)
                # Right-align headers (except the left-most one).
                if col_name != self.header_column:
                    value = " " + value
                row[col_name] = value
            return
        # Get the slice of the row that should be formated (i.e. the data columns).
        # Note that there might be other columns (e.g. added by dynamic data
        # modules) that should not be formated.
        row_slice = {col_name: row.get(col_name) for col_name in self.col_names}

        min_wins = self.get_min_wins(row_name)
        highlight = min_wins is not None
        colored = self.colored and highlight
        colors = get_elementwise_colors(row_slice, min_wins) if colored else None
        if highlight:
            min_max_values = get_elementwise_min_max(row_slice.values())
        else:
            min_max_values = (None, None)

        def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
            return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

        for col_name, value in row.items():
            color = None
            bold = False
            # Format data columns
            if col_name in row_slice:
                if colored:
                    color = rgb_fractions_to_html_colors(colors[col_name])
                elif (
                    highlight
                    and value is not None
                    and (
                        (is_close(value, min_max_values[0]) and min_wins)
                        or (is_close(value, min_max_values[1]) and not min_wins)
                    )
                ):
                    bold = True
            row[col_name] = self._format_cell(
                row_name, col_name, value, color, bold
            )

    def _format_cell(self, row_name, col_name, value, color, bold):
        """
        Return the formatted value for a single cell in the table.
        *row_name* and *col_name* specify the position of the cell and *value* is the
        unformatted value.
        Floats are rounded to two decimal places and lists are quoted. The *color* to
        render the result in can be given as a string and setting *bold* to true
        renders the value in bold.

        If a custom formatter is specified for this cell, it is used instead of this
        default format.
        """
        formatter = self.cell_formatters.get(row_name, {}).get(col_name)
        if formatter:
            return formatter.format_value(value)

        justify_right = isinstance(value, (float, int, list))

        def format_value(value):
            if isinstance(value, list):
                result = [format_value(val) for val in value]
                return result
            elif isinstance(value, float):
                return "{0:.{1}f}".format(value, self.digits)
            elif isinstance(value, int):
                return value
            else:
                result = str(value)

            # Only escape text if it doesn't contain LaTeX or HTML markup.
            if "''" in result or '""' in result:
                return result
            else:
                return markup.escape(result)

        value_text = format_value(value)

        if color is not None:
            if isinstance(value_text, list):
                value_text = "''[" + ", ".join([f"<span style=\"color:{col}\"> {val} </span>" for val, col in zip(value_text, color)]) + "]''"
            else:
                value_text = f"{{{value_text}|color:{color}}}"
        if bold:
            value_text = "**%s**" % value_text
        if justify_right:
            value_text = " " + value_text
        return value_text
