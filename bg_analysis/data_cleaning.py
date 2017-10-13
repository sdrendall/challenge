import StringIO
import numpy as np
import pandas as pd
from datetime import datetime

def motion_timestring_to_datetime(time_str):
  str_pattern = '%Y-%m-%dT%H:%M:%S.%f'
  time_str = time_str.split('+')[0]
  return datetime.strptime(time_str, str_pattern)

def glucose_timestring_to_datetime(time_str):
  str_pattern = '%Y-%m-%d %H:%M:%S'
  time_str = time_str.split('+')[0]
  return datetime.strptime(time_str, str_pattern)

def read_motion_tsv(f): 
  return pd.read_csv(
      f, 
      sep='\t', 
      header=None, 
      names=['time', 'stationary', 'walking', 'running', 'automotive', 'cycling']
  )

def motion_datastring_to_dataframe(datastr):
  buffered = StringIO.StringIO(datastr)
  df = read_motion_tsv(buffered) # premature optimization is the root of all evil....
  df['time'] = df['time'].map(motion_timestring_to_datetime)
  return df.set_index('time')
  
def as_vector(series):
    return series.as_matrix()[..., np.newaxis]

def timedelta_to_hours(td):
  return td.total_seconds()/(60*60)
