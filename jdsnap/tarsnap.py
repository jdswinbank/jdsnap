import datetime
import os
import shutil
import subprocess
import time
from .archive import Archive

__all__ = ["Tarsnap"]

DEFAULT_EXECUTABLE="tarsnap"
DEBUG = False

class Tarsnap(object):
    def __init__(self, prefix, exe=None, keyfile=None, cachedir=None):
        """
        Only handle archives when the name starts with ``prefix``.
        """
        self.prefix = prefix
        if exe:
            self.base_cmd = [os.path.realpath(exe)]
        else:
            self.base_cmd = [shutil.which(DEFAULT_EXECUTABLE)]
        if keyfile:
            self.base_cmd.extend(["--keyfile", os.path.realpath(keyfile)])
        if cachedir:
            self.base_cmd.extend(["--cachedir", os.path.realpath(cachedir)])

    def _exec_cmd(self, cmd):
        cmd = self.base_cmd + cmd
        if DEBUG:
            print(cmd)
        return subprocess.check_output(cmd).decode('utf-8')

    def create_archive(self, root, suffix=None):
        """
        Create an archive of the tree anchored at ``root``.

        If ``suffix`` is provided, archive will be named
        ``self.prefix-suffix``. Otherwise, we will use the current Unix time
        (seconds since the epoch) as a unique name.
        """
        if not suffix:
            suffix = str(time.time())
        archive_name = "-".join([self.prefix, suffix])
        self._exec_cmd(["-c", "-f", archive_name, root])
        return archive_name

    def list_archives(self):
        """
        Returns a list of Archives.

        datetimes are naive & in the system default timezone (can be
        over-ridden by setting the TZ environment variable.
        """
        archives = []
        for line in self._exec_cmd(["-v", "--list-archives"]).split('\n'):
            if line.startswith(self.prefix):
                name, date = line.split('\t')
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                archives.append(Archive(name, date))
        return archives

    def rm_archive(self, archive_name):
        """
        Delete ``archive_name``.
        """
        if not archive_name.startswith(prefix):
            raise Exception("Prefix mismatch: expected %s" % (self.prefix,))
        self._exec_cmd(["-d", "-f", archive_name])
