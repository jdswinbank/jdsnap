import os
import sys

import klaxon

from .date import YEAR, MONTH, WEEK, DAY
from .filter import filter_archives
from .tarsnap import Tarsnap


__all__ = ["manage_all_archives"]


def prune_archive(tarsnap_archive, intervals):
    """Remove unneeded archives.
    """
    all_archives = tarsnap_archive.list_archives()
    keep_archives = filter_archives(all_archives, intervals)
    delete_archives = set(all_archives) - set(keep_archives)
    for archive in delete_archives:
        print(f"Removing {archive}")
        tarsnap_archive.rm_archive(archive)


def manage_archive(name, path, *, exclude, tarsnap, debug):
    """Manage backups for a directory.

    Archive the files at ``path`` with to an archive named ``name``. Maintain
    a rolling history.
    """
    tarsnap = Tarsnap(name, exe=tarsnap, debug=debug)

    # Create new archive
    print(f"Createing new archive for {name}")
    tarsnap.create_archive(path, exclude=exclude)

    # Prune old archives
    print(f"Pruning old archives for {name}")
    prune_archive(tarsnap, [YEAR, MONTH, WEEK, DAY])


def manage_all_archives(archives, tarsnap, debug=False):
    """Manage backups for all directories.

    Parameters:
    ===========
    archives : `dict` [`str`, `dict`]
        Keys are the base names of archives. The associated value contains
        configuration information. This includes at least ``path``, and,
        optionally, ``exclude``.
    """
    for name, cfg in backup_locations.items():
        print(f"Processing {name}")
        try:
            manage_archive(
                name,
                cfg.get("path"),
                exclude=cfg.get("exclude", None),
                tarsnap=tarsnap,
                debug=debug,
            )
        except Exception as e:
            klaxon.klaxon(title="jdsnap backup failed", subtitle=name, message=str(e))
            print(f"  Failed: {e}", file=sys.stderr)
