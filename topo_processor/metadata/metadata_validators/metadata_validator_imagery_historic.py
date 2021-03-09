from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util.tiff import is_tiff

from .metadata_validator import MetadataValidator


class MetadataValidatorImageryHistoric(MetadataValidator):
    name = "validator.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_file):
            return False
        return True

    async def validate_metadata(self, item: Item) -> None:
        item.is_valid = True
        item.output_dir = item.stac_item.properties["linz:survey"]