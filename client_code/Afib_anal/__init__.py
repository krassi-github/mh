import datetime
from ._anvil_designer import Afib_analTemplate
from anvil import *
import anvil.server

import plotly.graph_objects as go
#from plotly.subplots import make_subplots
from .. import Data


class Afib_anal(Afib_analTemplate):
  id_title = ''
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Test on 09.09.2025  GPT rework 20-06-2025 ----------------------------------------
    # Задаваме `main_form` след създаване
    self.filter_1.set_main_form(self)
    clm_date = [c for c in self.data_grid_1.columns if c['title'] == 'date'][0]
    self.id_title = clm_date["id"]
    
    self.show_plot()
    self.show_grid()


  def render_data(self, user, rng, Tb=None, Te=None, Step=None, crawl=False):   #  show_range  
    # Form1.render_data(user, rng, Tb=None, Te=None, Step=None, crawl=Fals)
    r = Data.set_bp_list(user, fr=rng, Tb=Tb, Te=Te, Step=Step, crawl=crawl)
    if r < 0:
      self.label_2.text += f"  set_bp_list= {r}"
      self.label_2.foreground = "red"
      self.label_2.boldface = True

    if r < 0:
      pass    # UI message to be generated
    else:
      self.repeating_panel_1.items = [row for row in Data.bp_list if row.get("afib") is not None and row.get("afib") != ""]
      #self.repeating_panel_1.items = Data.bp_list
      # print(f"RP.items = {self.repeating_panel_1.items}")
      self.s_from.text = Data.loaded_from[:10]
      self.s_to.text = "-     " + Data.loaded_to[:10]
      self.s_tz.text = Data.zt_beg + " - " + Data.zt_end
      if Data.slice_step:
        self.s_step.text = Data.slice_step
      else:
        self.s_step.text = ''
      
      for i, c in enumerate(self.data_grid_1.columns):
        if c["id"] == self.id_title:
          if Data.slice_mode:
            self.data_grid_1.columns[i]["title"] = 'SLICE'
          else:
            self.data_grid_1.columns[i]["title"] = 'DATE'
      self.data_grid_1.columns = self.data_grid_1.columns 
      
      
  # Във форма Afib_anal, метод или бутон
  def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Plot(figure=fig))

  def show_grid(self):
    # self.repeating_panel_1.items = list(filter(lambda row: row.get("afib"), Data.bp_list))
    self.repeating_panel_1.items = [row for row in Data.bp_list if row.get("afib") is not None and row.get("afib") != ""]


  def show_move(self, direction):
    Tb, Te = anvil.server.call("times_calc", Data.current_range, \
                                 Data.loaded_from, Data.loaded_to, direction)
    self.label_2.text = f"{Tb}  {Te}  {Data.current_range} "
    te = datetime.datetime.strptime(Te,  "%Y/%m/%d %H:%M")
    #te -= datetime.timedelta(days=1)
    Te = te.strftime("%Y/%m/%d %H:%M")
    self.render_data("1001", Data.current_range, Tb, Te, crawl=True)
  
# Events handling ----------------------------------------------------------------------------------
  def back_click(self, **event_args):
    open_form("Form1")

  def b_up_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def b_dn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
    

