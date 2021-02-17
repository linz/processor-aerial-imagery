import rasterio
from rasterio.enums import ColorInterp

from topo_processor.factory.item import Item
from topo_processor.util.tiff import is_tiff

from .metadata_validator import MetadataValidator


class MetadataValidatorTiff(MetadataValidator):
    name = "validator.imagery.tiff"

    def is_applicable(self, item: Item) -> bool:
        return is_tiff(item.path)

    async def check_validity(self, item: Item) -> None:
        photo_type = item.stac_item.properties["linz:photo_type"]
        with rasterio.open(item.path) as tiff:
            if ColorInterp.gray in tiff.colorinterp and len(tiff.colorinterp) == 1:
                if photo_type != "B&W":
                    raise Exception(f"Validation failed. {item.path} has a wrong photo type")
            if all(item in [ColorInterp.red, ColorInterp.blue, ColorInterp.green] for item in tiff.colorinterp):
                if photo_type != "COLOUR":
                    raise Exception(f"Validation failed. {item.path} has a wrong photo type")
