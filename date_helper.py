from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_end_date(number_of_months: int):
    delta_month = 0 if number_of_months == 0 else number_of_months - 1
    return datetime.now().date() - relativedelta(months=delta_month)
