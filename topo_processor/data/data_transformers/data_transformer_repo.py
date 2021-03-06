import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.stac import Item
from topo_processor.util import time_in_ms

from .data_transformer import DataTransformer


class DataTransformerRepository:
    transformers: List[DataTransformer] = []
    lock = asyncio.Semaphore(5)

    def append(self, transformers: DataTransformer) -> None:
        self.transformers.append(transformers)

    async def transform_data(self, item: Item) -> None:
        async with self.lock:
            for transformer in self.transformers:
                if transformer.is_applicable(item):
                    start_time = time_in_ms()
                    try:
                        await transformer.transform_data(item)
                    except Exception as e:
                        item.add_error(str(e), transformer.name, e)
                        get_log().warning(f"Data Transform Failed: {e}", transformers=transformer.name)
                        return False
                    get_log().debug(
                        "Data Transformed",
                        duration=time_in_ms() - start_time,
                    )
