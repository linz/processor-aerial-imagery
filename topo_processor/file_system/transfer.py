from .get_fs import get_fs


def transfer_file(source_file: str, target_file: str):
    with get_fs(source_file).open(source_file, "rb") as f1:
        data = f1.read()
        with get_fs(target_file).open(target_file, "wb") as f2:
            f2.write(data)
