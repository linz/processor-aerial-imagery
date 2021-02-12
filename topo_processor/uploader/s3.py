import asyncio

import boto3
from linz_logger import get_log

from topo_processor.metadata.collection import Collection
from topo_processor.util import multihash_as_hex, time_in_ms, write_stac_object

s3 = boto3.client("s3")


async def upload_to_s3(collection: Collection, target: str):
    await upload_items(collection, target)
    await upload_collection(collection, target)


async def upload_items(collection: Collection, target: str):
    to_upload = []
    for item in collection.items:
        # TODO save to temp location
        # for metadata
        await write_stac_object(item, f"temp/{item.item_output_path}")
        hash_value = await multihash_as_hex(f"temp/{item.item_output_path}")
        to_upload.append(
            upload_file(f"temp/{item.item_output_path}", f"{item.item_output_path}", "application/json", hash_value, target)
        )
        # for data
        to_upload.append(
            upload_file(
                item.path,
                f"{item.asset_basename}.{item.asset_extension}",
                item.content_type,
                item.stac_item.properties["checksum:multihash"],
                target,
            )
        )
    await asyncio.gather(*to_upload)


async def upload_collection(collection: Collection, target: str):
    # TODO save to temp location
    await write_stac_object(collection, f"temp/{collection.collection_output_path}")
    hash_value = await multihash_as_hex(f"temp/{collection.collection_output_path}")
    await upload_file(
        f"temp/{collection.collection_output_path}",
        f"{collection.collection_output_path}",
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
