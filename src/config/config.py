# calculate_investment_scenario
import json
from dataclasses import dataclass

import numpy as np

from taipy import Config, Scope


class AssetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Asset):
            return {
                "__type__": "Asset",
                "name": obj.name,
                "distribution_type": obj.distribution_type,
                "mean_return": obj.mean_return,
                "std_dev": obj.std_dev,
            }
        return json.JSONEncoder.default(self, obj)


class AssetDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        if d.get("__type__") == "SaleRow":
            return Asset(
                name=d["name"],
                distribution_type=d["distribution_type"],
                mean_return=d["mean_return"],
                std_dev=d["std_dev"],
            )
        return d


@dataclass
class Asset:
    """Defines the risk and return characteristics of an investment product."""

    name: str
    distribution_type: str  # For now, always 'normal'
    mean_return: float  # Annual expected return (e.g., 0.08 for 8%)
    std_dev: float  # Volatility (e.g., 0.15 for 15%)


asset_nodes_config = Config.configure_json_data_node(
    id="assets", default_path="./data/assets.json", scope=Scope.GLOBAL
)
investment_scenario_node_config = Config.configure_data_node(
    id="investment_scenario",
)
