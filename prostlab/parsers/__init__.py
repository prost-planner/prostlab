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

def get_all_prost_parser_attributes():
    """ Return all attributes that are parsed by the ProstParser in 
    prostlab.parsers.

    """
    return [
        "parser_time",
        "search_time",
        "total_time",
        "total_reward",
        "average_reward",
        "round_reward",
    ]

def get_default_prost_parser_attributes():
    """ Return default attributes that are parsed by the ProstParser in 
    prostlab.parsers.

    """
    return [
        "parser_time",
        "search_time",
        "average_reward",
    ]

def get_all_thts_parser_attributes():
    """ Return all attributes that are parsed by the THTSParser in 
    prostlab.parsers.

    """
    return [
        "entries_prob_state_value_cache",
        "buckets_prob_state_value_cache",
        "entries_prob_applicable_actions_cache",
        "buckets_prob_applicable_actions_cache",
        "rem_steps_first_solved_state",
        "trials_first_relevant_state",
        "search_nodes_first_relevant_state",
        "perc_exploration_first_relevant_state",
    ]

def get_default_thts_parser_attributes():
    """ Return default attributes that are parsed by the THTSParser in 
    prostlab.parsers.

    """
    return [
        "rem_steps_first_solved_state",
        "trials_first_relevant_state",
    ]

def get_all_ids_parser_attributes():
    """ Return all attributes that are parsed by the IDSParser in 
    prostlab.parsers.

    """
    return [
        "ids_learned_search_depth",
        "entries_det_state_value_cache",
        "buckets_det_state_value_cache",
        "entries_det_applicable_actions_cache",
        "buckets_det_applicable_actions_cache",
        "entries_ids_reward_cache",
        "buckets_ids_reward_cache",
        "ids_avg_search_depth_first_relevant_state",
        "ids_total_num_runs",
        "ids_avg_search_depth_total",
    ]

def get_default_ids_parser_attributes():
    """ Return default attributes that are parsed by the IDSParser in 
    prostlab.parsers.

    """
    return [
        "ids_learned_search_depth",
    ]

def get_all_attributes_of_algorithm(algo):
    """ Return all attributes that are relevant for the algorithm *algo* and
    parsed by one of the Prost default parsers in prostlab.parsers.

    """
    result = ["ipc_score"] + get_all_prost_parser_attributes()
    if "THTS" in algo or "IPC2011" in algo or "IPC2014" in algo:
        result += get_all_thts_parser_attributes()

    if "IDS" in algo or "IPC2011" in algo or "IPC2014" in algo:
        result += get_all_ids_parser_attributes()
        
    return result

def get_default_attributes_of_algorithm(algo):
    """ Return default attributes that are relevant for the algorithm *algo*
    and parsed by one of the Prost default parsers in prostlab.parsers.

    """
    result = ["ipc_score"] + get_default_prost_parser_attributes()
    if "THTS" in algo or "IPC2011" in algo or "IPC2014" in algo:
        result += get_default_thts_parser_attributes()

    if "IDS" in algo or "IPC2011" in algo or "IPC2014" in algo:
        result += get_default_ids_parser_attributes()
        
    return result
