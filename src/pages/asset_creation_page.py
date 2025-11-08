import taipy.gui.builder as tgb

from algorithms import (
    create_new_asset,
    edit_asset,
    open_close_delete_asset_dialog,
    select_asset_for_edit,
)

with tgb.Page() as asset_creation_page:
    tgb.text("## **Manage** Assets", mode="md")

    tgb.text("## Edit Asset", mode="md")

    tgb.selector(
        "{selected_asset_for_edit}",
        lov="{asset_list}",
        dropdown=True,
        label="Select Asset",
        class_name="fullwidth plain",
        on_change=select_asset_for_edit,
    )
    with tgb.layout("1 1 1"):
        tgb.toggle(
            "{asset_for_edit_distribution_type}",
            lov=["normal", "lognormal"],
            label="asset type",
            class_name="fullwidth",
        )
        tgb.number(
            "{asset_for_edit_mean_return}",
            min=0,
            max=1,
            step=0.01,
            class_name="fullwidth",
        )
        tgb.number(
            "{asset_for_edit_std_dev}", min=0, max=1, step=0.01, class_name="fullwidth"
        )

    tgb.button(
        label="Update Asset",
        class_name="fullwidth plain",
        on_action=edit_asset,
    )

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

    tgb.data_node(
        "{asset_nodes}", show_history=False, show_properties=False, expanded=False
    )
