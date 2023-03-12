import anvil.server
import datetime
#    from . import Module1
all = True    # all - including records without values (measurements)
params = {}
'''INSERT INTO Params(key, descr, value1) values
('day1', "fixed ranges start on first day", 1),
('d_step', "day default step 1h", 60),
('w_step', "week default step 6h", 6*60),
('m_step', "month default step 1day", 24*60),
('m3_step', "3 months default step 1 day", 24*60),
('r_step', "range default step 1 month", 30*24*60),
('r_range', "default length of range 6m", 180),
('orange_sys', "systolic I threshold", 135),
('red_sys', "systolic II threshold", 140),
('orange_dia', "diastolic I threshold", 85),
('red_dia', "diastolic II threshold", 90),
('red_mean', "mean pressure threshold", 100)'''
sd_descr = {}     # values = [1] modules names
sysdata = {}      # values = [2] text messages
'''INSERT INTO SysData(key, descr, value) values
('-111', "import_data()", "open DB error"),
('-110', "import_data()", "open DB error"),
('-109', "import_data()", "processing error"),
('-108', "import_data()", "no records error"),
('-107', "import_data()", "no NEW records")'''
ALL 




time_from = ""
time_to = ""
zone_items = [("ALL", 0), ("08:00 - 16:00", 1),  ("16:00 - 24:00", 2), ("00:00 - 08:00", 3)]
current_zone = 0
current_day = ""
current_range = ''
loaded_from = ""
loaded_to = ""

bp_dat = []
bp_date = []
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


def load_params():
  global params
  global time_to
  global time_from

  params = anvil.server.call("get_params")
  r, tt = anvil.server.call("get_last_date")
  if r :
    return(r)  
  elif not params:
    return(-260)     # !! WRONG return
  else:
    time_to = tt
    tb = datetime.datetime.strptime(tt, "%Y/%m/%d %H:%M") - datetime.timedelta(days=params["r_range"])
    time_from = datetime.datetime.strftime(tb, "%Y/%m/%d %H:%M")
    return(0)   
  

def load_sysdata():
  global sd_descr
  global sysdata

  sysdata, sd_descr = anvil.server.call("get_sysdata")
  if not sysdata: 
    r = -22
  elif not sd_descr:
    r = -23
  else:
    r = 0
  return(r)  
    

def set_bp_list(user_id, fr=None, Tb=None, Te=None, Step=None, crawl=False):
  global x_data  # !! Иначе не прехвърля данните (за разлика от променливите, работещи с append)
  global y_values
  global params
  global all
  global bp_list
  global bp_date
  global bp_sys
  global bp_dia
  global bp_sys_add
  global bp_mean
  global bp_colors
  global current_range
  global loaded_from      # loaded data time stamp FROM (? x_data VS y_values[1])
  global loaded_to        # loaded data time stamp TO

  # Retreive data from DB
  # current_range = fr    
  r, x_data, y_values = anvil.server.call("prep_plot", user_id, fr=fr, Tb=Tb, Te=Te, Step=Step, \
                                          Average=False, fill_empty=False, crawl=crawl)
  #data format: ["          ", "                ", (s); (d); (p); (m); (a)]
  #print(x_data)
  #print(y_values) 
  bp_list = []
  bp_date = []
  bp_sys = []
  bp_dia = []
  bp_sys_add = []
  bp_mean = []
  bp_colors = []
  if not r:       
    for i in range(len(y_values)):      
      if all or y_values[i][2]:    #        
        bp_list.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})        
        bp_date.append(y_values[i][1])
        bp_sys.append(y_values[i][2])
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
    loaded_from = x_data[0]     # test x_data alternatively
    loaded_to = x_data[-1]
  return(r)
  

def set_summary(user_id, fr=None, Tb=None, Te=None, crawl=False):
  global bp_summary
  global all
  x_data = []
  y_values = []

  bp_summary = []
  r, x_data, y_values = anvil.server.call("prep_plot", user_id, fr=fr,
                                          Tb=Tb, Te=Te, Average=True, fill_empty=False, crawl=crawl)
  print(f"Summ  {Tb} !! {Te}  X= {x_data} #  Y= {y_values}")
  if not r:       
    for i in range(len(y_values)):      
      if y_values[i][2]:    #        
        bp_summary.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})
  return(r)

    




  
