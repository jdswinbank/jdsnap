import datetime
import sys
from typing import List, Optional

import klaxon  # type: ignore

from .date import YEAR, MONTH, WEEK, DAY
from .filter import filter_archives
from .tarsnap import Tarsnap
from .types import ArchiveConfigurations


__all__ = ["manage_all_archives"]


def prune_archive(tarsnap: Tarsnap, intervals: List[datetime.timedelta]) -> None:
    """Remove unneeded archives.
    """
    all_archives = tarsnap.list_archives()
    keep_archives = filter_archives(all_archives, intervals)
    delete_archives = set(all_archives) - set(keep_archives)
    for archive in delete_archives:
        print(f"Removing {archive.name}")
        tarsnap.rm_archive(archive)


def manage_archive(
    name: str, path: str, *, exclude: Optional[str], tarsnap_path: str, debug: bool
) -> None:
    """Manage backups for a directory.

    Archive the files at ``path`` with to an archive named ``name``. Maintain
    a rolling history.
    """
    tarsnap = Tarsnap(name, exe=tarsnap_path, debug=debug)

    # Create new archive
    print(f"Creating new archive for {name}")
    tarsnap.create_archive(path, exclude=exclude)

    # Prune old archives
    print(f"Pruning old archives for {name}")
    prune_archive(tarsnap, [YEAR, MONTH, WEEK, DAY])


def manage_all_archives(
    archives: ArchiveConfigurations, tarsnap_path: str, debug=False
) -> None:
    """Manage backups for all directories.

    Parameters:
    ===========
    archives : `dict` [`str`, `dict`]
        Keys are the base names of archives. The associated value contains
        configuration information. This includes at least ``path``, and,
        optionally, ``exclude``.
    """
    for name, cfg in archives.items():
        print(f"Processing {name}")
        try:
            manage_archive(
                name,
                cfg["path"],
                exclude=cfg.get("exclude"),  # None),
                tarsnap_path=tarsnap_path,
                debug=debug,
            )
        except Exception as e:
            klaxon.klaxon(title="jdsnap backup failed", subtitle=name, message=str(e))
            print(f"  Failed: {e}", file=sys.stderr)
