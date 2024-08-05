from datetime import datetime, timedelta


def parse_dates(dates) -> list:
    new_dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    new_dates.sort()
    return new_dates


def calculate_stay(entries_list, exits_list, future_entry, process_date: bool = True):
    if process_date:
        entries_list = parse_dates(entries_list)
        exits_list = parse_dates(exits_list)
        future_entry = parse_dates([future_entry])[0]
    if (len(entries_list) - len(exits_list)) == 1:
        # You entered but did not exit yet
        exits_list.append(future_entry)
    if len(entries_list) != len(exits_list):
        raise Exception(f'The entries is not equal to number of exists!')
    # Calculate past stays within the last 180 days from the future entry date
    days_stayed = 0
    start_period = future_entry - timedelta(days=180)
    for entry, exit in zip(entries_list, exits_list):
        if exit < entry:
            raise Exception(f'Wrong dates the {entry=} should be before {exit}')
        if exit > start_period:
            stay_start = max(entry, start_period)
            stay_end = min(exit, future_entry)
            days_stayed += (stay_end - stay_start).days
    # Calculate remaining allowed days
    return days_stayed


def calculate_allowed_stay(entries_list, exits_list, future_entry) -> int:
    if not entries_list:
        return 90
    entries_list = parse_dates(entries_list)
    exits_list = parse_dates(exits_list)
    future_entry = parse_dates([future_entry])[0]
    allow_days: int = 0
    calculate_point = future_entry
    entries_list.append(future_entry)
    while calculate_stay(
            entries_list,
            exits_list + [calculate_point],
            calculate_point,
            process_date=False
    ) < 90:
        allow_days += 1
        calculate_point = future_entry + timedelta(days=allow_days)

    return allow_days

# Example usage
# entries_dates = ["2024-02-01", "2024-04-07", "2024-05-18"]
# exits_dates = ["2024-03-28", "2024-05-07", "2024-06-21"]
# future_entry = "2024-09-01"

# allowed_days = calculate_allowed_stay(entries_dates, exits_dates, future_entry)
# print(f"Allowed stay duration based on future entry date {future_entry}: {allowed_days} days")
