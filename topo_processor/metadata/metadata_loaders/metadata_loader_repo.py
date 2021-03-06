import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.stac import Asset
from topo_processor.util import time_in_ms

from .metadata_loader import MetadataLoader


class MetadataLoaderRepository:
    loaders: List[MetadataLoader] = []
    lock = asyncio.Semaphore(5)

    def append(self, loader: MetadataLoader) -> None:
        self.loaders.append(loader)

    async def load_metadata(self, asset: Asset) -> None:
        async with self.lock:
            for loader in self.loaders:
                if loader.is_applicable(asset):
                    start_time = time_in_ms()
                    try:
                        await loader.load_metadata(asset)
                        if not asset.is_valid:
                            break
                    except Exception as e:
                        asset.add_error(str(e), loader.name, e)
                        get_log().warning(f"Metadata Load Failed: {e}", loader=loader.name)
                        return
                    get_log().debug(
                        "Metadata Loaded",
                        loader=loader.name,
                        duration=time_in_ms() - start_time,
                    )
