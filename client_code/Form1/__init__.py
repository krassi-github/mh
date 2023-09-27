import datetime
from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import plotly.graph_objects as go
from .. import Data
from ..afibs_g import afibs_g

def error_handler(err):
  alert(str(err), title="An issue has occurred")
  
class Form1(Form1Template):  
  def __init__(self, **properties):
    set_default_error_handling(error_handler)   # for TESTING
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.    
    #self.b_up.width = "80"
    #self.b_up.text = "   "
    #self.b_dn.width = "60"
    self.column_panel_1.width = "90%"
    self.button_1.width = "60%"
    self.column_panel_2.row_spacing = 4
    self.flow_panel_2.border =  "border-bottom: 6px solid red"  # ""border-top-style: dotted"  # "solid"       #
    self.color_rows(self.repeating_panel_1)
    self.render_data("1001", 'd')
  
  def color_rows(self, rep):    
    for i, r in enumerate(rep.get_components()):
      if not i%2:
        r.background = "rgba(69,183,249,0.2)"  #'theme:Gray 200'     

  def show_summary(self):
    tot = 0
    if Data.bp_summary:
      self.lb_21.text = Data.bp_summary[0]["date"][:10]
      self.lb_22.text = Data.bp_summary[0]["sys"]
      self.lb_23.text = Data.bp_summary[0]["dia"]
      self.lb_24.text = Data.bp_summary[0]["pul"]
      self.lb_25.text = Data.bp_summary[0]["mean"]
      self.lb_26.text = Data.bp_summary[0]["afib"]
      self.lb_26.foreground = "red"
      
      if int(self.lb_22.text) >= Data.params["red_sys"]:
        self.lb_22.foreground = "red"
      elif int(self.lb_22.text) >= Data.params["orange_sys"]:
        self.lb_22.foreground = "orange"
      else:
        self.lb_22.foreground = "black"      
      if int(self.lb_23.text) >= Data.params["red_dia"]:
        self.lb_23.foreground = "red"
      elif  int(self.lb_23.text) >= Data.params["orange_dia"]:
        self.lb_23.foreground = "orange"
      else:
        self.lb_23.foreground = "black"
      if int(self.lb_25.text) > Data.params["red_mean"]:
        self.lb_25.foreground = "red"
      else:
        self.lb_25.foreground = "black"
    else:
      self.lb_21.text = ''
      self.lb_22.text = ''
      self.lb_23.text = ''
      self.lb_24.text = ''
      self.lb_25.text = ''
      self.lb_26.text = ''

    tot = Data.green_cntr + Data.orange_cntr + Data.red_cntr
    if not tot:
      print(f"from Forms1.show_summary() {Data.bp_summary}")
      tot = 1

    self.lb_31.text = "        "
    self.lb_31.background = Data.c_green
    self.lb_33.text = "        "
    self.lb_33.background = Data.c_orange
    self.lb_35.text = "        "
    self.lb_35.background = Data.c_red
    self.lb_32.text = str(round(100*Data.green_cntr/tot)) + "%"
    self.lb_34.text = str(round(100*Data.orange_cntr/tot)) + "%"
    self.lb_36.text = str(round(100*Data.red_cntr/tot)) + "%"

    
  def render_data(self, user, rng, Tb=None, Te=None, Step=None, crawl=False):   #  show_range    
    r = Data.set_bp_list(user, fr=rng, Tb=Tb, Te=Te, Step=Step, crawl=crawl)
    if r:
      self.label_2.text += f"  set_bp_list= {r}"
      self.label_2.foreground = "red"
      self.label_2.boldface = True
    r1 = Data.set_summary(user, fr=rng, Tb=Tb, Te=Te, crawl=crawl)
    if r1:
      self.label_2.text += f"  set_summary= {r1} "
      self.label_2.foreground = "red"
      self.label_2.boldface = True
    if r or r1:
      pass    # UI message to be generated
    else:
      self.repeating_panel_1.items = Data.bp_list
      # print(f"RP.items = {self.repeating_panel_1.items}")
      self.s_from.text = Data.loaded_from[:10]
      self.s_to.text = "-     " + Data.loaded_to[:10]
      self.s_tz.text = Data.zt_beg + " - " + Data.zt_end
      self.show_summary()
      self.plot_1_show()

  def show_move(self, direction):
    Tb, Te = anvil.server.call("times_calc", Data.current_range, \
                               Data.loaded_from, Data.loaded_to, direction)
    self.label_2.text = f"{Tb}  {Te}  {Data.current_range} "
    te = datetime.datetime.strptime(Te,  "%Y/%m/%d %H:%M")
    #te -= datetime.timedelta(days=1)
    Te = te.strftime("%Y/%m/%d %H:%M")
    self.render_data("1001", Data.current_range, Tb, Te, crawl=True)

  def b_up_click(self, **event_args):
    #self.app_title.text = f"UP time_from= {Data.time_from}  time_to= {Data.time_to}"
    self.show_move("up")    

  def b_dn_click(self, **event_args):
    #self.app_title.text = f"DN time_from= {Data.time_from}  time_to= {Data.time_to}"
    self.show_move("dn")    
  
  def plot_1_show(self):
    self.label_1.text = (f"init x_data_len: {len(Data.x_data)} y_values_len: {len(Data.y_values)}\
    bp_list: {len(Data.bp_list)}  bp_mean: {len(Data.bp_mean)}")
    if Data.all:
      on_x = Data.x_data
    else:
      on_x = Data.bp_date

    if len(Data.bp_list) and len(Data.bp_mean):
      fig = go.Figure(
        data=[
          go.Bar(
            name="BP-D",
            x=on_x,    # 10-02-2023  x_data
            y=Data.bp_dia,      # , bp_list[2] it works
            offsetgroup=0,
            marker = dict(color = "rgba(10, 10, 10, 0.05)", )
          ),
          go.Bar(
            name="BP-S",
            x=on_x,    # 10-02-2023  x_data
            y=Data.bp_sys_add,
            offsetgroup=0,
            base = Data.bp_dia,          
            marker = dict(color=Data.bp_colors, )
          ),
          go.Scatter(
            name="BP-M",
            x=on_x,    # 10-02-2023  x_data
            y=Data.bp_mean,
            marker = dict(color = "rgba(0, 0, 200, 0.9)", )
          ) 
        ],                
        layout=go.Layout(       
          title="Артериално налягане",        
          yaxis=dict(range=[60, max(Data.bp_sys)], title="BP mm/Hg"),
          showlegend=False,
          # xaxis=dict(title="Време"),
          # expand the graphs
          margin=dict(
              l=50, #left margin
              r=50, #right margin
              # b=50, #bottom margin
              t=50, #top margin
          ),
        )
      )
      self.plot_1.figure = fig
      self.plot_1.visible = True
    else:
      self.plot_1.visible = False    # NO data to plot
  

    
    #  snipets
    '''          
      layout=go.Layout(       
        title="Артериално налягане",
        yaxis_title="BP mm/Hg",
        yaxis_range=[60, 200],
        yaxis=dict(range=[30, 170)
        showlegend=False,
        #xaxis_title="Време"    
      )
    
    !!!
    layout_boxplots = go.Layout(margin=dict(t=50, b=50, l=150, r=50),    width=500,
    height=300,
    font=dict(family='Open Sans', size=14, color='#176db6'),
    showlegend=False,
    yaxis=dict(range=[-5, max(data1)]),
    yaxis2 = dict(range=[-5,max(data2)]),
    yaxis3 = dict(range=[-5,max(data3)]),
    updatemenus=updatemenus_boxplots
)
    MEAN preassure
        go.Scatter(
          name="BP-M",
          x=Data.x_data,
          y=Data.bp_mean,
          marker = dict(color = "rgba(0, 0, 200, 0.9)", )
        ) 
    '''
    '''
    self.plot_1.data = [
    go.Bar(
    x = Data.bp_dat,
    y = Data.bp_sys,
    name="BP",
    color= 'rgb(16, 32, 77)',
    marker = dict(
      color= 'rgba(200,09, 0, 0.2)',         # color= 'rgb(16, 32, 77)'      
      )
    ), 
    ]
    '''

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Analysis')

  