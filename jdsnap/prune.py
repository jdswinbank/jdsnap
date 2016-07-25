import datetime
from jdsnap.date import DEFAULT_DATEFMT, date_from_name

__all__ = ["filter_archive_list"]

def uniqify(input_list):
    return list(set(input_list))

def filter_archive_list(archives, intervals, prefix, datefmt=DEFAULT_DATEFMT,
                        keep_all=None, current_date=None):
    """
    Given a list of known archives, return only those which should be kept.
    """
    # We will never performing pruning of two or less archives. Simply return
    # the uniqified list of inputs.
    archives = uniqify(archives)
    if len(archives) <= 2:
        return archives

    get_date = lambda archive: date_from_name(archive, prefix, datefmt)

    current_date = current_date or datetime.datetime.utcnow()
    archives.sort(key=get_date)
    keep = [archives[0]]  # Always include the oldest archive
    processed_archive = 0

    for interval in intervals:
        for archive in archives[processed_archive+1:-1]:
            # If the current date is inside the interval, we move to the next.
            if (current_date - interval) < get_date(keep[-1]):
                break

            # If the _next_ archive is going to be more than interval after
            # the last archive, we should keep this one.
            elif (get_date(archives[processed_archive+2])
                  - get_date(keep[-1])) > interval:
                keep.append(archive)

            # Keep everything within the last keep_all.
            elif keep_all and (get_date(archive) + keep_all) >= current_date:
                keep.append(archive)

            # We can discard this archive.
            else:
                pass

            processed_archive += 1

    keep.append(archives[-1])  # Always include the newest archive
    return keep
