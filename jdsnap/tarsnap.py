import datetime
import os
import subprocess
import time
from .archive import Archive

__all__ = ["Tarsnap"]

class Tarsnap(object):
    def __init__(self, prefix, *, exe, keyfile=None,
                 cachedir=None, debug=False):
        """
        Only handle archives when the name starts with ``prefix``.
        """
        self.prefix, self.base_cmd, self.debug = prefix, [exe], debug
        if keyfile:
            self.base_cmd.extend(["--keyfile", os.path.realpath(keyfile)])
        if cachedir:
            self.base_cmd.extend(["--cachedir", os.path.realpath(cachedir)])

    def _exec_cmd(self, cmd):
        cmd = self.base_cmd + cmd
        if self.debug:
            cmd.insert(1, "-v")
            print(cmd)
        return subprocess.check_output(cmd).decode('utf-8')

    def create_archive(self, root, suffix=None, exclude=None):
        """
        Create an archive of the tree anchored at ``root``.

        If ``suffix`` is provided, archive will be named
        ``self.prefix-suffix``. Otherwise, we will use the current Unix time
        (seconds since the epoch) as a unique name.

        If ``exclude`` is provided, it will be passed to the ``tarsnap
        --exclude`` option.
        """
        if not suffix:
            suffix = str(time.time())
        archive_name = "-".join([self.prefix, suffix])
        cmd = ["-c", "-H", "-f", archive_name, root]
        if exclude:
            cmd.insert(-1, "--exclude")
            cmd.insert(-1, exclude)
        self._exec_cmd(cmd)
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
                name, date = line.split('\t')[:2]
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                archives.append(Archive(name, date))
        return archives

    def rm_archive(self, archive):
        """
        Delete ``archive.name``.
        """
        if not archive.name.startswith(self.prefix):
            raise Exception("Prefix mismatch: expected %s" % (self.prefix,))
        self._exec_cmd(["-d", "-f", archive.name])
