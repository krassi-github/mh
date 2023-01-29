from ._anvil_designer import Test_MAINTemplate
from anvil import *
import anvil.server

class Test_MAIN(Test_MAINTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
