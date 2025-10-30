from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server


class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


'''# YearSummaryRowTemplate
class YearSummaryRowTemplate(YearSummaryRowTemplateTemplate):
  def item_change(self, **event_args):
    rec = self.item or {}
    # events (цяло число)
    self.lbl_events.text = f"{int(rec.get('N_measurements', 0))}"
    # afib_minutes (2 знака след десетичната)
    self.lbl_afib_minutes.text = f"{float(rec.get('AFIB_minutes', 0.0)):.2f}"
    # aii като промили (‰)
    aii = float(rec.get('AII', 0.0))
    self.lbl_aii.text = f"{aii * 1000:.1f}\u2030"   # напр. 5.3‰
    # година (ако имаш и етикет)
    self.lbl_year.text = f"{rec.get('year', '')}"
'''