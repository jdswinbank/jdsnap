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

    for interval in intervals:
        # If the current date is inside the interval and this is not the
        # last interval, we move to the next interval
        if ((current_date - interval) < keep[-1].date
            and interval is not intervals[-1]):
            continue
        for i, archive in enumerate(archives[1:-1], 1):
            # If the _next_ archive is going to be more than interval after
            # the last archive, we should keep this one.
            if (archives[i+1].date - keep[-1].date) > interval:
                keep.append(archive)

    keep.append(archives[-1])
    return uniqify(keep)
