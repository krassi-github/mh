from ._anvil_designer import impTemplate
from anvil import *
import anvil.server
from .. import Data

class imp(impTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    r1, all_recs, last_date = anvil.server.call("db_status")
    self.label_1.text = "All Records:  " + str(all_recs)
    self.last.text = last_date[1]
    self.width = "90%"


  def file_loader_1_change(self, file, **event_args):
    if file.content_type != "text/csv":
      alert(f"{file.name} is not csv file", title="Invalid file")
      self.file_loader_1.clear()
      self.label_1.text = '.CSV file'
      return(0)
    self.label_1.text = file.name
    r = anvil.server.call("import_csv", file)
    if r < 0:
      msg = Data.sysdata[str(r)]
      alert(f"{msg}", title="System Message")
      self.file_loader_1.clear()
      self.label_1.text = '.CSV file'
      return(0)
    self.file_loader_1.clear()
    r1, all_recs, last_date = anvil.server.call("db_status")
    self.label_1.text = str(r) + ' / ' + str(all_recs)
    self.last.text = last_date
    Data.load_params()
    self.timer_1.interval = 10

  def file_loader_1_lost_focus(self, **event_args):
    self.label_1.text = '.CSV file'

  def timer_1_tick(self, **event_args):
    self.label_1.text = '.CSV file'
    self.timer_1.interval = 0
