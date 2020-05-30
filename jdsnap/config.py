import argparse
import json
import os.path
import shutil
import typing

from .types import ArchiveConfigurations

__all__ = ["parse_args", "read_config"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automated backups.")
    parser.add_argument("--tarsnap", default=shutil.which("tarsnap"))
    parser.add_argument(
        "--config",
        type=argparse.FileType(),
        default=os.path.expanduser("~/.jdsnap.json"),
    )
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def read_config(cfg_file: typing.TextIO) -> ArchiveConfigurations:
    return json.load(cfg_file)
