import datetime
from ._anvil_designer import Afib_analTemplate
from anvil import *
import anvil.server
from anvil import ColumnPanel  # gp 21-09-2025

import plotly.graph_objects as go
#from plotly.subplots import make_subplots
from .. import Data

# 26-09-2025 При проблем с прехвърлянето на Data,current_range между формите може
# да се приложи GPT MH_project -> AfibWork 1 решението
class Afib_anal(Afib_analTemplate):
  id_title = ''
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.column_panel_3.width = 520
    self.data_grid_1.columns_dict['col_aii']['visible'] = True
    self.data_grid_1.columns = list(self.data_grid_1.columns)  # apply

    # Test on 09.09.2025  GPT rework 20-06-2025 ----------------------------------------
    # Задаваме `main_form` след създаване
    self.filter_1.set_main_form(self)
    clm_date = [c for c in self.data_grid_1.columns if c['title'] == 'date'][0]
    self.id_title = clm_date["id"]

    self.show_y_summary()
    self.show_plot()
    self.show_grid()

  
  def render_data(self, user, rng, Tb=None, Te=None, Step=None, crawl=False):   #  show_range  
    r = Data.set_bp_list(user, fr=rng, Tb=Tb, Te=Te, Step=Step, crawl=crawl)    
    if r < 0:
      self.label_2.text += f"  set_bp_list= {r}"
      self.label_2.foreground = "red"
      self.label_2.boldface = True
    else:
      rows = [row for row in Data.bp_list \
              if row.get("afib") is not None and row.get("afib") != ""] 
      items = [{**row, "i": i} for i, row in enumerate(rows, start=0)] # index inserted to each
#     #if Data.slice_mode:
        #items = [row for row in items if row.get("afibs")]    # filtering afibs 31-10-2025
      self.repeating_panel_1.items = items
      
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
# Left data grid - yearly afibs summary
# [{'year': 2025, 'N_measurements': 2450, 'S_afib_units': 13, 'AII': 0.005306, 'AFIB_minutes': 16.25}]
  def show_y_summary(self):
    self.repeating_panel_2.items = Data.afibs_year_summary("all")

  def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')
    #self.plot_1.width = 700    # 800
    #self.plot_1.height = 500   # 630
    self.plot_1.figure = fig

    
# Right data grid - List of afib events selected by Filter  
  def show_grid(self):
    # self.repeating_panel_1.items = list(filter(lambda row: row.get("afib"), Data.bp_list))
    self.repeating_panel_1.items = [row for row in Data.bp_list if row.get("afib") is not None and row.get("afib") != ""]


  def show_move(self, direction):    # NEW from the Form1
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
    self.show_move("up")

  def b_dn_click(self, **event_args):
    self.show_move("dn")

  # ************************************************************************************************
# Useful snipets / alternatives
# Previous one
  '''  def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')

    self.column_panel_2.clear()
    p = Plot(figure=fig)
    p.width = 800                   # <-- ширина на компонента (px)
    p.height = 630
    #p(full_width_row=True = True)
    self.column_panel_2.add_component(p)'''
  ''' def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')
    fig.update_layout(
      title={"text": "---------- Events", "x": 0.5, "xanchor": "center", "y": 0.98, "yanchor": "top"},
      width=1800
    )
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Plot(figure=fig))  # To change for plot position & size ??  
  ''' 

  '''def show_plot(self, **event_args):
    fig = anvil.server.call('get_afib_figure')
    plot_component = Plot(figure=fig)
  
    wrapper = ColumnPanel()
    wrapper.role = "plot-wrapper"
    wrapper.add_component(plot_component) 
    self.column_panel_2.clear()
    self.column_panel_2.add_component(wrapper)
  '''
