from datetime import datetime, timezone
from zoneinfo import ZoneInfo

COLOMBIA_TZ = ZoneInfo("America/Bogota")

def get_colombia_time() -> datetime:
    return datetime.now(timezone.utc).astimezone(COLOMBIA_TZ)

def format_colombia_time(
    dt: datetime,
    fmt: str = "%Y-%m-%d %H:%M:%S"
) -> str:

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    bogota_dt = dt.astimezone(COLOMBIA_TZ)
    return bogota_dt.strftime(fmt)

def format_colombia_time_readable(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    bogota_dt = dt.astimezone(COLOMBIA_TZ)
    return bogota_dt.strftime("%b %d, %Y %I:%M %p COT")

def format_colombia_time_short(dt: datetime) -> str:
    """
    Returns: '8/3/2025 4:24 PM'
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    bogota_dt = dt.astimezone(COLOMBIA_TZ)
    return bogota_dt.strftime("%m/%d/%Y %I:%M %p")

def format_colombia_time_iso(dt: datetime) -> str:
    """
    Returns: '2025-08-03T16:24:10-05:00'
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    bogota_dt = dt.astimezone(COLOMBIA_TZ)
    return bogota_dt.isoformat()
