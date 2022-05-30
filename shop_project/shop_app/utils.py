from datetime import datetime


def time_is_valid(str_time):
    try:
        datetime.strptime(str_time, '%H:%M:%S')
    except ValueError:
        return False
    return True


def str_time_to_object_time(str_time):
    datetime_object = datetime.strptime(str_time, '%H:%M:%S')
    datetime_object = datetime.time(datetime_object)
    return datetime_object
