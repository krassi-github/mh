from ._anvil_designer import impTemplate
from anvil import *
import anvil.server

class imp(impTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.width = "90%"


  def file_loader_1_change(self, file, **event_args):
    my_media = file    
    print(f'content_type: {my_media.content_type}')
    print(f'length: {my_media.length} bytes')
    print(f'name: {my_media.name}')
    print(f'raw bytes: {my_media.get_bytes()[:15]} ...')
    r = anvil.server.call("import_csv", file)
    self.file_loader_1.clear()
    self.label_1.text = r

  def file_loader_1_lost_focus(self, **event_args):
    self.label_1.text = ''

