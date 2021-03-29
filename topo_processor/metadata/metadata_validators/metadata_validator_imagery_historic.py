import os

from linz_logger import get_log

from topo_processor.stac import DataType, Item
from topo_processor.util import is_tiff

from .metadata_validator import MetadataValidator


class MetadataValidatorImageryHistoric(MetadataValidator):
    name = "validator.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        return True

    async def validate_metadata(self, item: Item) -> None:
        for asset in item.assets:
            parent_folder = os.path.basename(os.path.dirname(asset.path))
            if not parent_folder == asset.item.collection.title:
                get_log().info(
                    "Metadata survey does not match image parent folder",
                    metadata_survey=asset.item.collection.title,
                    parent_folder=parent_folder,
                    source_path=asset.path,
                )
