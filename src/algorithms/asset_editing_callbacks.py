from taipy.gui import notify

from algorithms.callback_helpers import cond_eq_notify, cond_in_notify


def delete_asset(state):
    with state as s:
        asset_nodes_dict = s.asset_nodes.read()
        del asset_nodes_dict[s.selected_asset_for_deletion]
        s.asset_list = list(asset_nodes_dict.keys())
        s.selected_asset_for_edit = s.asset_list[0]
        s.asset_nodes.write(asset_nodes_dict)


def open_close_delete_asset_dialog(state, vars, payload):
    if payload.get("args") == [0]:  # Selected YES to delete asset
        delete_asset(state)
    with state as s:
        if s.selected_asset_for_deletion == "":
            return
        current = s.delete_asset_dialog
        s.delete_asset_dialog = not current


def create_new_asset(state):
    with state as s:
        asset_name = s.new_asset_name
        if cond_eq_notify(s, (asset_name, ""), "New Asset Needs a Name!"):
            return
        asset_dict = s.asset_nodes.read()
        assets = asset_dict.keys()
        if cond_in_notify(s, (asset_name, assets), "This Asset Exists!"):
            return
        asset_dict = _add_empty_asset(asset_dict, asset_name)
        s.asset_nodes.write(asset_dict)
        s.asset_list = list(asset_dict.keys())
        s.new_asset_name = ""
        notify(s, "s", "New Asset Created!")


def _add_empty_asset(asset_dict, asset_name):
    asset_dict[asset_name] = {
        "distribution_type": "lognormal",
        "mean_return": 0.00,
        "std_dev": 0.00,
    }
    return asset_dict


def select_asset_for_edit(state):
    with state as s:
        asset_nodes_dict = s.asset_nodes.read()
        asset_dict = asset_nodes_dict.get(s.selected_asset_for_edit)
        s.asset_for_edit_distribution_type = asset_dict.get("distribution_type")
        s.asset_for_edit_mean_return = asset_dict.get("mean_return")
        s.asset_for_edit_std_dev = asset_dict.get("std_dev")


def edit_asset(state):
    with state as s:
        if s.selected_asset_for_edit == "":
            return
        asset_nodes_dict = s.asset_nodes.read()
        asset_dict = asset_nodes_dict.get(s.selected_asset_for_edit)
        asset_dict["distribution_type"] = s.asset_for_edit_distribution_type
        asset_dict["mean_return"] = s.asset_for_edit_mean_return
        asset_dict["std_dev"] = s.asset_for_edit_std_dev

        asset_nodes_dict[s.selected_asset_for_edit] = asset_dict
        s.asset_nodes.write(asset_nodes_dict)

        _clear_asset_edit(state)


def _clear_asset_edit(state):
    with state as s:
        s.selected_asset_for_edit = ""
        s.asset_for_edit_distribution_type = ""
        s.asset_for_edit_mean_return = 0
        s.asset_for_edit_std_dev = 0
