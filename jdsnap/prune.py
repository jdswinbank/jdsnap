import datetime
from operator import attrgetter

__all__ = ["filter_archives"]

def uniqify(arg):
    return list(set(arg))

def filter_archives(archives, intervals, keep_all_within=None, current_date=None):
    """
    Return a list of archive names which should be kept.

    ``archives`` is a list of ``jdsnap.Archive``s.
    ``intervals`` is a list of intervals.
    Everything within ``keep_all_within`` of the current date is kept.
    """
    if len(archives) <= 2:
        return [archive[0] for archive in archives]

    if not current_date:
        current_date = datetime.datetime.utcnow()
    archives = sorted(archives, key=attrgetter("date"))
    keep = [archives[0]]  # Always include the oldest archive.
    processed_archive = 0

    for interval in intervals:
        for archive in archives[processed_archive+1:-1]:
            # If the current date is inside the interval and this is not the
            # last interval, we move to the next interval
            if ((current_date - interval) < keep[-1].date
                and interval is not intervals[-1]):
                break

            # If the _next_ archive is going to be more than interval after
            # the last archive, we should keep this one.
            elif (archives[processed_archive+2].date - keep[-1].date) > interval:
                keep.append(archive)

            # Keep everything within the last keep_all.
            elif keep_all_within and (archive.date + keep_all_within) >= current_date:
                    keep.append(archive)

            # Discard this archive
            else:
                pass

            processed_archive += 1

    keep.append(archives[-1])
    return uniqify(keep)
