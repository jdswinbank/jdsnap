import datetime
from operator import attrgetter

__all__ = ["filter_archives"]


def uniqify(arg):
    return list(set(arg))


def filter_archives(archives, intervals, current_date=None):
    """
    Return a list of archive names which should be kept.

    ``archives`` is a list of ``jdsnap.Archive``s.
    ``intervals`` is a list of intervals.
    """
    if len(archives) <= 2:
        return [archive for archive in archives]

    if not current_date:
        current_date = datetime.datetime.utcnow()
    archives = sorted(archives, key=attrgetter("date"))
    keep = [archives[0]]  # Always include the oldest archive.
    prev_interval = None

    for interval in intervals:
        for i, archive in enumerate(archives[1:-1], 1):
            # If the archive date is within the interval of the current date,
            # we skip it: it'll be caught on the next interval.
            if (current_date - interval) < archive.date:
                continue

            # If the archive date is outside the previous interval of the
            # current date, we skip it.
            if prev_interval and (archive.date < (current_date - prev_interval)):
                continue

            # If the _next_ archive is going to be more than interval after
            # the last archive, we should keep this one.
            if (archives[i + 1].date - keep[-1].date) > interval:
                keep.append(archive)

        prev_interval = interval

        # Always maintain the list in chronological order.
        keep = sorted(keep, key=attrgetter("date"))

    keep.append(archives[-1])
    return sorted(uniqify(keep), key=attrgetter("date"))
