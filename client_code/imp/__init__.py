from ._anvil_designer import impTemplate
from anvil import *
import anvil.server
from .. import Data

import json
import anvil.js
from anvil import alert
#from anvil.js.window import a7GetMeasurements
from anvil.js.window import (
a7GetMeasurements,
b6GetMeasurements,
)


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
    self.timer_1.interval = 20

  def file_loader_1_lost_focus(self, **event_args):
    self.label_1.text = '.CSV file'

  def timer_1_tick(self, **event_args):
    self.label_1.text = '.CSV file'
    self.timer_1.interval = 0

  @handle("button_1", "click")
  def button_1_click(self, **event_args):    # GP's name is a7_sync_click
    try:
      result = a7GetMeasurements()
  
      records = json.loads(
        result.recordsJson
      )
  
      sync = anvil.server.call(
        "a7_import",
        records,
        False
      )
  
      if sync["collisions"] > 0:
        alert(
          (
            f"User {sync['device_user']}\n"
            f"Read: {sync['read']}\n"
            f"Collisions: {sync['collisions']}\n\n"
            "Nothing was imported."
          ),
          title="A7 Sync - ERROR"
        )
        return
  
      if sync["imported"] == 0:
        text = (
          f"User {sync['device_user']}\n"
          f"Read: {sync['read']}\n"
          f"Already present: "
          f"{sync['duplicates']}\n\n"
          "Database is up to date."
        )
  
      else:
        text = (
          f"User {sync['device_user']}\n"
          f"Read: {sync['read']}\n"
          f"Already present: "
          f"{sync['duplicates']}\n"
          f"New imported: "
          f"{sync['imported']}\n\n"
          "Sync completed."
        )
  
      alert(
        text,
        title="A7 Sync"
      )
  
    except Exception as err:
      alert(
        str(err),
        title="A7 Sync - ERROR"
      )

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    try:
      result = b6GetMeasurements()
  
      text = (
        f"User: {result.user}\n"
        f"Records: {result.records}\n\n"
        f"Period:\n"
        f"{result.periodStart}\n"
        f"{result.periodEnd}\n\n"
        f"AFIB: {result.afib}\n"
        f"IHB: {result.ihb}\n"
        f"AFIB+IHB: {result.afibIhb}\n\n"
        f"AFIB records:\n"
        f"{result.afibText}"
      )
  
      alert(
        text,
        title="B6 BLE TEST"
      )
  
    except Exception as err:
      alert(
        str(err),
        title="B6 BLE TEST - ERROR"
      )
      
 