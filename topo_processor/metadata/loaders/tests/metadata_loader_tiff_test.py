import asyncio
import os

from topo_processor.metadata.loaders.metadata_loader_tiff import MetadataLoaderTiff
from topo_processor.stac.collection import Collection
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item


def test_add_metadata():
    tiff_path = os.path.join(os.getcwd(), "test_data", "tiffs", "399", "CROWN_399_E_49.tiff")
    collection = Collection(DataType.ImageryHistoric)
    item = Item(tiff_path, collection)
    item.asset_basename = "399/1234"
    loader = MetadataLoaderTiff()
    assert loader.is_applicable(item)

    asyncio.run(loader.add_metadata(item))
    assert item.stac_item.properties["proj:epsg"] is None
    assert len(item.stac_item.assets) == 1
    assert item.stac_item.assets["image"].properties["linz:image_height"] == 9