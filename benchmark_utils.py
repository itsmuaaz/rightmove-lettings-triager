from datetime import datetime, timedelta

def get_next_benchmark_time() -> datetime:
    """
    Calculates the next benchmark time for commute calculations.
    Benchmark: The upcoming Tuesday at 09:00 AM.
    
    If today is Tuesday and before 09:00 AM, returns today at 09:00 AM.
    If today is Tuesday and after 09:00 AM, returns next Tuesday at 09:00 AM.
    Otherwise, returns the next Tuesday at 09:00 AM.
    """
    now = datetime.now()
    target_weekday = 1  # Tuesday
    
    days_ahead = (target_weekday - now.weekday() + 7) % 7
    
    if days_ahead == 0:
        # Today is Tuesday
        if now.hour >= 9:
            days_ahead = 7
            
    next_benchmark = now + timedelta(days=days_ahead)
    return next_benchmark.replace(hour=9, minute=0, second=0, microsecond=0)
