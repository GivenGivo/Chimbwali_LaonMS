from datetime import timedelta

def generate_repayment_schedule(start_date, exempt_day='SUNDAY'):
    dates = []
    current_date = start_date
    count = 0

    while len(dates) < 26:
        if exempt_day.upper() == 'SUNDAY' and current_date.weekday() != 6:
            dates.append(current_date)
        elif exempt_day.upper() == 'SATURDAY' and current_date.weekday() != 5:
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates
