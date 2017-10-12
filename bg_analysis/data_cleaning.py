from datetime import datetime

def motion_timestring_to_datetime(time_str):
  str_pattern = '%Y-%m-%dT%H:%M:%S.%f'
  time_str = time_str.split('+')[0]
  return datetime.strptime(time_str, str_pattern)

def glucose_timestring_to_datetime(time_str):
  str_pattern = '%Y-%m-%d %H:%M:%S'
  time_str = time_str.split('+')[0]
  return datetime.strptime(time_str, str_pattern)
