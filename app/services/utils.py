import pandas as pd

__all__ = ['SvcUtils']


class SvcUtils():
    def get_interval_col(start_date: str, end_date: str) -> str:
        """Determine the appropriate interval for the given date range."""
        if not start_date or not end_date:
            return 'Y'

        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        diff = (end - start).days

        if diff <= 7:
            return 'D'
        elif diff <= 90:
            return 'W'
        elif diff <= 365:
            return 'M'
        elif diff <= 730:
            return 'Q'
        else:
            return 'Y'
