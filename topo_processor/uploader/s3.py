import asyncio
import os

import boto3
from linz_logger import get_log

from topo_processor.stac.collection import Collection
from topo_processor.util import multihash_as_hex, time_in_ms, write_stac_object

s3 = boto3.client("s3")


async def upload_to_s3(collection: Collection, target: str):
    await upload_items(collection, target)
    await upload_collection(collection, target)


async def upload_items(collection: Collection, target: str):
    to_upload = []
    for item in collection.items:
        # for metadata
        await write_stac_object(item, os.path.join(collection.temp_dir, item.metadata_file))
        hash_value = await multihash_as_hex(os.path.join(collection.temp_dir, item.metadata_file))
        to_upload.append(
            upload_file(
                os.path.join(collection.temp_dir, item.metadata_file),
                item.metadata_file,
                "application/json",
                hash_value,
                target,
            )
        )
        # for data
        to_upload.append(
            upload_file(
                item.source_dir,
                f"{item.asset_basename}.{item.asset_extension}",
                item.content_type,
                item.stac_item.properties["checksum:multihash"],
                target,
            )
        )
    await asyncio.gather(*to_upload)


async def upload_collection(collection: Collection, target: str):
    await write_stac_object(collection, os.path.join(collection.temp_dir, collection.metadata_file))
    hash_value = await multihash_as_hex(os.path.join(collection.temp_dir, collection.metadata_file))
    await upload_file(
        os.path.join(collection.temp_dir, collection.metadata_file),
        collection.metadata_file,
        "application/json",
        hash_value,
        target,
    )


async def upload_file(filepath: str, key: str, content_type: str, hash_value: str, bucket: str):
    start_time = time_in_ms()
    s3.upload_file(
        Filename=filepath,
        Bucket=bucket,
        Key=key,
        ExtraArgs={"ContentType": content_type, "Metadata": {"hash": hash_value}},
    )
    get_log().debug(
        "S3 Multipart File Uploaded",
        duration=time_in_ms() - start_time,
        Bucket=bucket,
        Key=key,
    )
