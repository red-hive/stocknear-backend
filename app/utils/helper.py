from datetime import datetime, timedelta, time, date
import os
import orjson
import pytz

def check_market_hours():

    holidays = [
        "2024-01-01", "2024-01-15", "2024-02-19", "2024-03-29",
        "2024-05-27", "2024-06-19", "2024-07-04", "2024-09-02",
        "2024-11-28", "2024-12-25"
    ]
    
    # Get the current date and time in ET (Eastern Time)
    et_timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(et_timezone)
    current_date_str = current_time.strftime('%Y-%m-%d')
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_day = current_time.weekday()  # Monday is 0, Sunday is 6

    # Check if the current date is a holiday or weekend
    is_weekend = current_day >= 5  # Saturday (5) or Sunday (6)
    is_holiday = current_date_str in holidays

    # Determine the market status
    if is_weekend or is_holiday:
        return False #"Market is closed."
    elif 9 <= current_hour < 16 or (current_hour == 17 and current_minute == 0):
        return True #"Market hours."
    else:
        return False #"Market is closed."


def load_latest_json(directory: str):
    """Load the JSON file corresponding to today's date (New York time) or the last Friday if today is a weekend."""
    try:
        # Get today's date in New York timezone
        ny_tz = pytz.timezone("America/New_York")
        today_ny = datetime.now(ny_tz).date()

        # Adjust to Friday if today is Saturday or Sunday
        if today_ny.weekday() == 5:  # Saturday
            today_ny -= timedelta(days=1)
        elif today_ny.weekday() == 6:  # Sunday
            today_ny -= timedelta(days=2)

        # Construct the filename based on the adjusted date
        target_filename = f"{today_ny}.json"
        target_file_path = os.path.join(directory, target_filename)

        # Check if the file exists and load it
        if os.path.exists(target_file_path):
            with open(target_file_path, 'rb') as file:
                return orjson.loads(file.read())
        else:
            print(f"No JSON file found for the target date: {target_filename}")
            return []  # File for the target date not found
    except Exception as e:
        print(f"Error loading JSON file for the target date: {e}")
        return []
