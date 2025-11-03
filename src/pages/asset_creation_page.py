import taipy.gui.builder as tgb
from taipy.gui import notify


# TODO: Clean these functions and apply some DRY
# TODO (2): Add an Edit Node Section and remove Data Node element
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
        if asset_name == "":
            notify(s, "w", "New Asset Needts to Have a Name!")
            return
        asset_nodes_dict = s.asset_nodes.read()
        if asset_name in asset_nodes_dict.keys():
            notify(s, "w", "This Asset Name Exists Already!")
            return
        asset_nodes_dict[asset_name] = {
            "distribution_type": "normal",
            "mean_return": 0.00,
            "std_dev": 0.00,
        }
        s.asset_nodes.write(asset_nodes_dict)
        s.asset_list = list(asset_nodes_dict.keys())
        s.new_asset_name = ""
        notify(s, "s", "New Asset Created!")


with tgb.Page() as asset_creation_page:
    tgb.text("## Manage Assets", mode="md")

    tgb.data_node("{asset_nodes}", show_history=False, show_properties=False)
    tgb.html("hr")
    tgb.text("## Create New Asset", mode="md")
    with tgb.layout("1 1"):
        tgb.input(
            "{new_asset_name}",
            lov="{asset_list}",
            dropdown=True,
            label="New Asset Name",
            class_name="fullwidth plain",
        )
        tgb.button(
            label="Create New Asset",
            class_name="fullwidth plain",
            on_action=create_new_asset,
        )

    tgb.html("hr")
    tgb.text("## Delete Asset", mode="md")
    with tgb.layout("1 1"):
        tgb.selector(
            "{selected_asset_for_deletion}",
            lov="{asset_list}",
            dropdown=True,
            label="Select Asset",
            class_name="fullwidth plain",
        )
        tgb.button(
            label="Delete Asset",
            class_name="fullwidth plain",
            on_action=open_close_delete_asset_dialog,
        )
        tgb.dialog(
            "{delete_asset_dialog}",
            on_action=open_close_delete_asset_dialog,
            title="Do you really want to delete this asset?",
            labels="Yes!;No",
        )
