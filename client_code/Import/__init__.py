from ._anvil_designer import ImportTemplate
from anvil import *
import anvil.server
import anvil.media

path = "c:\microlife"


class Import(ImportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def file_loader_1_change(self, file, **event_args):
    my_media = file    
    print(f'content_type: {my_media.content_type}')
    print(f'length: {my_media.length} bytes')
    print(f'name: {my_media.name}')
    print(f'raw bytes: {my_media.get_bytes()[:15]} ...')
    self.file_loader_1.clear()
    r = anvil.server.call("import_csv", file)
    
    


