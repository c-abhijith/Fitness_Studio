from datetime import datetime, timedelta
import pytz

def convert_timezone(date_str, time_str, duration_minutes, current_tz_str, target_tz_str):
    datetime_str = f"{date_str} {time_str}"
    naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    
    current_tz = pytz.timezone(current_tz_str)
    localized_datetime = current_tz.localize(naive_datetime)
    
    target_tz = pytz.timezone(target_tz_str)
    converted_start = localized_datetime.astimezone(target_tz)
    
    converted_end = converted_start + timedelta(minutes=duration_minutes)

    return {
        "converted_date": converted_start.strftime("%Y-%m-%d"),
        "converted_start_time": converted_start.strftime("%H:%M:%S"),
        "converted_end_time": converted_end.strftime("%H:%M:%S"),
        "duration_minutes": duration_minutes  # <-- Add this line
    }
