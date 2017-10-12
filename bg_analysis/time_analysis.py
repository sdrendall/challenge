import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bg_analysis import consts

class AnalysisEngine(object):
  def __init__(self, initial_time=datetime.now(), log_interval=timedelta(minutes=15)):
    self.last_log_time = initial_time
    self.last_eval_time = initial_time
    self.log_interval = log_interval
    self.reset_time_acc()
    self.activity_state = {state: 0 for state in consts.STATES}
    self.activity_table = pd.DataFrame(self.time_acc, index=[initial_time])
    
  def process_line(self, time_state_tuple):
    time, new_state = time_state_tuple
    since_output = time - self.last_log_time
    while since_output > self.log_interval:
      # complete current interval
      end_of_current = self.last_log_time + self.log_interval
      self.update_time_acc(end_of_current) # dump time to accumulator
      self.log_to_activity_table(end_of_current) # log and reset accumulator
      since_output = time - self.last_log_time # last_log_time is increasing so this terminates

    self.update_time_acc(time)
    self.update_state(new_state)

  def log_to_activity_table(self, log_time):
    new_row = pd.DataFrame(self.time_acc, index=[log_time])
    self.activity_table = pd.concat((self.activity_table, new_row))
    self.reset_time_acc()
    self.last_log_time = log_time

  def update_time_acc(self, time):
    elapsed_time = time - self.last_eval_time
    for activity, active in self.activity_state.iteritems():
      if active:
        self.time_acc[activity] += elapsed_time
    self.last_eval_time = time

  def update_state(self, state):
    self.activity_state = {activity: active for activity, active in state.iteritems()}

  def reset_time_acc(self):
    self.time_acc = {state: timedelta(0) for state in consts.STATES}

