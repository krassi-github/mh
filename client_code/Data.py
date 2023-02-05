import anvil.server
#    from . import Module1

bp_dat = []
bp_sys = []
bp_dia = []
bp_sys_add = []
bp_pul = []
bp_mean = []
bp_n = []
bp_colors = []
bp_list = []
bp_summary = []
x_data = []
y_values = []

params = {}

def load_params():
  global params
  params = anvil.server.call("get_params")

def set_bp_list(user_id):
  global x_data  # !! Иначе не прехвърля данните (за разлика от променливите, работещи с appens)
  global y_values
  global params

  # Retreive data from DB
  r, x_data, y_values = anvil.server.call("prep_plot", user_id, Tb="2021/07/22 00:00", Te="2021/08/23 23:59",\
                                Step=1440, fill_empty=False)
  #data format: ["          ", "                ", (s); (d); (p); (m); (a)]
  #print(y_values)
  #print(x_data)
  if not r:
    all = False    # all - including records without values (measurements)   
    for i in range(len(y_values)):      
      if all or y_values[i][2]:    #        
        bp_list.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})        
        bp_dia.append(y_values[i][3])        
        bp_sys_add.append(y_values[i][2] - y_values[i][3])
        if y_values[i][2] >= params["red_sys"] or y_values[i][3] >= params["red_dia"]:
          bp_colors.append("rgba(255,0,0, 0.8)")        
        elif y_values[i][2] >= params["orange_sys"] or y_values[i][3] >= params["orange_dia"]:
          bp_colors.append("rgba(245,195,39, 1.0)")
        else:
          bp_colors.append("rgba(0,255,0, 1.0)")
        
        if y_values[i][5]:
          bp_mean.append(y_values[i][5])
        elif len(bp_mean):          
          for k in (y_values[i:]):
            if k[5]:
              bp_mean.append(k[5])
              break
        elif not len(bp_mean):
          bp_mean.append(None)       
  return(r)
  
# ===============================================================================================================================
# Time filters
t_range = ''

fixed_range = ''
time_from = None
time_to = None
d_default = 60
w_default = 6*60
m_default = 24*60
m3_default = 24*60
r_default = 30*24*60

current_day = ""
current_range = ''


