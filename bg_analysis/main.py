import os
import pickle
import pandas as pd
from datetime import datetime
from datetime import timedelta
from itertools import imap
from sys import stdin, stdout

from bg_analysis import consts
from bg_analysis import time_analysis
from bg_analysis import data_cleaning

# some constants to make life easier
data_start = datetime(2017, 5, 23, 0, 0, 0)
engine_init = data_start - timedelta(days=2)

def main():
  from sys import argv
  if len(argv) < 1:
    print "A model path must be specified!"
    return

  model_file = open(argv[1])
  model = pickle.load(model_file)

  engine = time_analysis.AnalysisEngine(
    initial_time=engine_init,
    log_interval=timedelta(minutes=15)
  )

  for line in stdin.readlines():
    as_df = data_cleaning.motion_datastring_to_dataframe(line)
    # iterating over as_df rows pusts it into the proper format for engine.process_line, even though it is only a single line
    engine.process_line(as_df.iterrows().next())
    current_walking = engine.get_most_recent_bin(
      bin_size=timedelta(days=2),
      activities=['walking']
    )['walking']
    current_walking = current_walking.map(data_cleaning.timedelta_to_hours)
    risk = model.predict_proba(data_cleaning.as_vector(current_walking))[0][1]
    stdout.write('{:03.03f}'.format(risk) + os.linesep)


if __name__ == '__main__':
  main()
