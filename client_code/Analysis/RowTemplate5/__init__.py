from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
from .. import Data

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    print("RowTemplate5 ____________________________________")
    self.init_components(**properties)
    self.row_spacing = 0
    print(f"Data.comp_summary  {Data.comp_summary}")
    print(f" Locally  {self.item}")
    self.no.text = self.item["no"]
    self.s1.text = self.item['s1']
    self.s2.text = self.item["s2"]
    self.d1.text = self.item["d1"]
    self.d2.text = self.item["d2"]
    self.p1.text = self.item["p1"]
    self.p2.text = self.item["p2"]
    self.m1.text = self.item["m1"]
    self.m2.text = self.item["m2"]
    self.a1.text = self.item["a1"]
    self.a2.text = self.item["a2"]

