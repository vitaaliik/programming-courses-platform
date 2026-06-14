from datetime import UTC

from zoneinfo import ZoneInfo


KYIV_TZ = ZoneInfo("Europe/Kyiv")


def to_kyiv_time(dt):

    if not dt:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    return dt.astimezone(KYIV_TZ)