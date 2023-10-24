import anvil.server
import datetime
#    from . import Module1
all = True    # all - including records without values (measurements)
#              initialized (to False) in __init__() of Filter
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

c_red = "rgba(255,0,0, 0.8)"
c_orange = "rgba(245,195,39, 1.0)"
c_green = "rgba(0,255,0, 1.0)"

sd_descr = {}     # values = [1] modules names
sysdata = {}      # values = [2] text messages
'''INSERT INTO SysData(key, descr, value) values
('-111', "import_data()", "open DB error"),
('-110', "import_data()", "open DB error"),
('-109', "import_data()", "processing error"),
('-108', "import_data()", "no records error"),
('-107', "import_data()", "no NEW records")'''

zones = [] 
''' record per zone. elements:
(type, key, beg, end)'''
zone_items = []               # [("ALL", "s0"), ("08:00 - 16:00", "c1"),  ("16:00 - 24:00", 2), ("00:00 - 08:00", 3)]
'''INSERT INTO Zones(type, key, beg, end) values as per 24-09-2023
("standard", "s_0", "00:00", "00:00"),
("standard", "s_1", "08:00", "16:00"),
("standard", "s_2", "16:00", "23:59"),
("standard", "s_3", "00:00", "08:00"),'''
custom_zone_items = []
'''
("custom", "c_1", "08:00", "12:00"),
("custom", "c_2", "11:00", "14:00"),
("custom", "c_3", "12:00", "17:00"),
("custom", "c_4", "17:00", "21:00")'''
current_zone = ''   # current time_zone
zt_beg = "08:00"    # current values of time_zones
zt_end = "16:00"

# filter_a (Analysis Form) Data
uom_items = [('Day', "d"), ("Week", "w"), ("Month", "m")]
uom = ''
max_number = (99, )    # max value of number (in period length)
number = 0
step = 0
Tb1 = ""
Tb2 = ""
Te1 = ""
Te2 = ""


time_from = ""
time_to = ""
current_day = ""
current_range = ''
loaded_from = ""
loaded_to = ""
loaded_from2 = ""
loaded_to2 = ""

comp_list = []    #[{"n", "no", " s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}]
# Data set 1
bp_date = []    # operational arrays for plotting
bp_sys = []     # systolic
bp_dia = []     # diastolic
bp_sys_add = [] # additive for plotting systolic (over the diastolic)
bp_pul = []     # puls
bp_mean = []    # mean pressure
bp_afib = []
bp_n = []
bp_colors = []   # collors
bp_list = []     # main data list [{}]
bp_summary = []  # summary
afibs = []       # afib events
x_data = []      # time data (X axis)
y_values = []    # blood pressure values
purple_cntr = 0  # color_counters (correspond to BP ranges)
red_cntr = 0     
orange_cntr = 0
green_cntr = 0

# Data Set 2
comp_summary = []  #[{"no", " s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}]
bp_date2 = []    # operational arrays for plotting
bp_sys2 = []     # systolic
bp_dia2 = []     # diastolic
bp_sys_add2 = [] # additive for plotting systolic (over the diastolic)
bp_pul2 = []     # puls
bp_mean2 = []    # mean pressure
bp_afib2 = []
bp_n2 = []
bp_colors2 = []   # collors
# data row [{"no", " s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}]
bp_list2 = []     # main data list [{}]
bp_summary2 = []  # summary
afibs2 = []       # afib events
x_data2 = []      # time data (X axis)
y_values2 = []    # blood pressure values
purple_cntr2 = 0  # color_counters (correspond to BP ranges)
red_cntr2 = 0     
orange_cntr2 = 0
green_cntr2 = 0

def load_params():
  global params
  global time_to
  global time_from

  params = anvil.server.call("get_params")
  r, tt = anvil.server.call("get_last_date")
  if r :
    return(-300+r)
  elif not params:
    return(-321)     
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
    r = -322
  elif not sd_descr:
    r = -323
  else:
    r = 0
  return(r)


def load_zones():
  global zones; global zone_items; global custom_zone_items;  

  z = anvil.server.call("get_zones")
  if not z:
    r = -325
  else:    
    zones = z
    zone_items = []
    custom_zone_items = []
    for r in z:
      if r[0] == "standard":
        zone_items.append((r[2]+' - '+r[3], r[1]))
      elif r[0] == "custom":
        custom_zone_items.append((r[2]+' - '+r[3], r[1]))
      else:
        return(-326)
    r = 0
  return(r)


def set_zone(zone):
  global zones; global current_zone; global zt_beg; global zt_end

  current_zone = zone
  for i in zones:
    if i[1] == zone:    # search the zone_keys
      zt_beg = i[2]
      zt_end = i[3]   

# *************************************************************************************    
# Load data funcs
# Data Block 1 filled
def set_bp_list(user_id, fr=None, Tb=None, Te=None, Step=None, crawl=False):
  global x_data  # !! Иначе не прехвърля данните (за разлика от променливите, работещи с append)
  global y_values
  global params
  global all
  global bp_list
  global bp_date
  global bp_sys
  global bp_dia
  global bp_pul
  global bp_sys_add
  global bp_mean
  global bp_colors
  global current_range
  global loaded_from      # loaded data time stamp FROM (? x_data VS y_values[1])
  global loaded_to        # loaded data time stamp TO
  global zt_beg           # beg of time zone
  global zt_end           # end of time zone
  global purple_cntr
  global red_cntr
  global orange_cntr
  global green_cntr

  # Retreive data from DB
  if zt_beg == "00:00" and zt_end == "23:59":
    zb = None
    ze = None
  else:
    zb = zt_beg
    ze = zt_end
  r, x_data, y_values = anvil.server.call("prep_plot", user_id, fr=fr, Tb=Tb, Te=Te, Step=Step, \
                        Average=False, fill_empty=False, crawl=crawl, zt_beg=zb, zt_end=ze)
  #data format: ["          ", "                ", (s); (d); (p); (m); (a)]
  #print(x_data)
  #print(y_values) 
  bp_list = []      # "date", "SYS", "DIA", "PUL", "MEA", "afib"
  bp_date = []
  bp_sys = []
  bp_dia = []
  bp_pul = []
  bp_sys_add = []
  bp_mean = []
  bp_colors = []
  green_cntr = 0
  orange_cntr = 0
  red_cntr = 0
  purple_cntr = 0
  if not r:       
    for i in range(len(y_values)):      
      if all or y_values[i][2]:    #        
        bp_list.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})        
        bp_date.append(y_values[i][1])
        bp_sys.append(y_values[i][2])
        bp_dia.append(y_values[i][3])
        bp_pul.append(y_values[i][4])
        bp_sys_add.append(y_values[i][2] - y_values[i][3])
        if y_values[i][2] >= params["red_sys"] or y_values[i][3] >= params["red_dia"]:
          bp_colors.append(c_red)
          red_cntr += 1
        elif y_values[i][2] >= params["orange_sys"] or y_values[i][3] >= params["orange_dia"]:
          bp_colors.append(c_orange)
          orange_cntr += 1
        else:
          bp_colors.append(c_green)
          green_cntr += 1
        
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
    # 20-06-2023
    #loaded_to = datetime.datetime.strptime(loaded_to, "%Y/%m/%d %H:%M") - datetime.timedelta(minutes=1)
    #loaded_to = datetime.datetime.strftime(loaded_to, "%Y/%m/%d %H:%M")
  return(r)
  
# -------------------------------------------------------------------------------------------------------------------------------
def set_summary(user_id, fr=None, Tb=None, Te=None, crawl=False):
  global bp_summary
  global all
  global zt_beg           # beg of time zone
  global zt_end           # end of time zone
  x_data = []
  y_values = []
  
  # Retreive data from DB
  bp_summary = []
  if zt_beg == "00:00" and zt_end == "23:59":
    zb = None
    ze = None
  else:
    zb = zt_beg
    ze = zt_end
  r, x_data, y_values = anvil.server.call("prep_plot", user_id, fr=fr,
                        Tb=Tb, Te=Te, Average=True, fill_empty=False, crawl=crawl, zt_beg=zb, zt_end=ze)
  # ======= print(f"Summ  {Tb} !! {Te}  X= {x_data} #  Y= {y_values}")
  if not r:       
    for i in range(len(y_values)):      
      if y_values[i][2]:    #        
        bp_summary.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})
  return(r)


def afib_details(row_date, L1=None, L2=None):
  global bp_list, bp_list2
  global afibs

  if L2:
    bp_ = bp_list2
    row_date = L2
  else:
    bp_ = bp_list

  afibs = []; r = 0
  #print(f"len bp_ {len(bp_)}"); print(bp_)
  for b in bp_:
    if b['date'] == row_date:
      a = b['afib']
      if a:
        afib_value = 1 if a == "AFIB" else int(a[:-2])    # more afibs are possible
        r, afib_rows = anvil.server.call("get_afibs", row_date, afib_value)
        for i in range(len(afib_rows)):
          afibs.append({"date": afib_rows[i][0], "sys":afib_rows[i][1], "dia":afib_rows[i][2],\
                  "pul":afib_rows[i][3], "mean":afib_rows[i][4]})
      else:
        r = 0
        afibs = "No AFIB on this row"
  if not r:
    return(afibs)
  else:
    return(f"DB issue {r}")

# ****************************************************************************************
# Load Data for Comparison
# Data Blocks 1 and 2 filled
def set_comp_list(object: str, number: int, uom: str, Step: int, Tb1: str, Tb2: str) -> int:
  
  global x_data, y_values, params, all, bp_list, bp_date, bp_sys, bp_dia, bp_sys_add, bp_mean,\
  bp_colors, current_range, loaded_from, loaded_to, zt_beg, zt_end, purple_cntr, red_cntr,\
  orange_cntr, green_cntr, bp_pul
  global bp_date2, bp_sys2, bp_dia2, bp_sys_add2, bp_pul2, bp_mean2, bp_n2, bp_colors2, bp_list2,\
  bp_summary2, afibs2, x_data2, y_values2, purple_cntr2, red_cntr2, orange_cntr2, green_cntr2,\
  loaded_from2, loaded_to2
  global comp_list, Te1, Te2
  global bp_afib, bp_afib2

  comp_list = []
  bp_list2 = []      
  bp_date2 = []
  bp_sys2 = []
  bp_dia2 = []
  bp_pul2 = []
  bp_sys_add2 = []
  bp_mean2 = []
  bp_afib2 = []
  bp_colors2 = []
  green_cntr2 = 0
  orange_cntr2 = 0
  red_cntr2 = 0
  purple_cntr2 = 0
  p1 = 0; p2 = 0
  '''
  if zt_beg == "00:00" and zt_end == "23:59":
    zb = None
    ze = None
  else:
    zb = zt_beg
    ze = zt_end 
  '''
  Te1, Te2 = anvil.server.call("periods_calc", number, uom, Step, Tb1=Tb1, Tb2=Tb2 )
  
  # prep data Block 2
  # р2, x_data, y_values = anvil.server.call("prep_plot", object, Tb=Tb2, Te=Te2, Step=Step, zt_beg=zb, zt_end=ze)
  p2 = set_bp_list(object, fr=None, Tb=Tb2, Te=Te2, Step=Step, crawl=False)
  x_data2 = x_data
  y_values2 = y_values
  bp_list2 = bp_list
  bp_date2 = bp_date
  bp_sys2 = bp_sys
  bp_dia2 = bp_dia
  bp_pul2 = bp_pul
  bp_sys_add2 = bp_sys_add
  bp_mean2 = bp_mean
  bp_afib2 = bp_afib
  bp_colors2 = bp_colors
  green_cntr2 = green_cntr
  orange_cntr2 = orange_cntr
  red_cntr2 = red_cntr
  purple_cntr2 = purple_cntr
  loaded_from2 = loaded_from
  loaded_to2 = loaded_to
  
  # prep Data Block 1
  # р1, x_data, y_values = anvil.server.call("prep_plot", object, Tb=Tb1, Te=Te1, Step=Step, zt_beg=zb, zt_end=ze)
  p1 = set_bp_list(object, fr=None, Tb=Tb1, Te=Te1, Step=Step, crawl=False)
  if p2 or p1:
    # Data prep error
    m = f"set_comp_list() p2= {p2}  p1= {p1}"
    anvil.serrver.call("mh_log", -901, m)
    return(-901)

  # Generate comp_list  #[{"n", "no", "date2", "s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}]
  len1= len(y_values);  len2= len(y_values2)
  if len1 >= len2:
    min_len = len2-1
  else:
    min_len = len1-1
  # print(f"set_comp_list() => Len1= {len(y_values)}  Len2= {len(y_values2)} min_len= {min_len}")
  for i in range(min_len):
    if all or y_values[i][2]:    #
      comp_list.append({"n": i, "no": y_values[i][1], "date2": y_values2[i][1], "s1":y_values[i][2],\ 
                        "s2":y_values2[i][2], "d1":y_values[i][3],  "d2":y_values2[i][3], "p1":y_values[i][4], \
                        "p2":y_values2[i][4],"m1":y_values[i][5], "m2":y_values2[i][5], "a1":y_values[i][6], "a2":y_values2[i][6]})        

  return(0)

# ----------------------------------------------------------------------------------------------
def set_comp_summary(object: str, number: int, uom: str, Step: int, Tb1: str, Tb2: str) -> int:
  global comp_summary, bp_summary, bp_summary2, bp_sys, bp_dia, bp_pul, bp_mean, bp_afib
  global all, bp_sys2, bp_dia2, bp_pul2, bp_mean2, bp_afib2
  global zt_beg  # beg of time zone
  global zt_end  # end of time zone
  x_data = []
  y_values = []
  x_data2 = []
  y_values2 = []
  p1 = 0; p2 = 0

  bp_summary = []
  bp_summary2 = []
  comp_summary = []
  # Retreive data from DB
  if zt_beg == "00:00" and zt_end == "23:59":
    zb = None
    ze = None
  else:
    zb = zt_beg
    ze = zt_end

  Te1, Te2 = anvil.server.call("periods_calc", number, uom, Step, Tb1=Tb1, Tb2=Tb2)

  # prep data Block 2
  р2, x_data2, y_values2 = anvil.server.call("prep_plot", object, Tb=Tb2, Te=Te2, Step=Step,
                                           Average=True, zt_beg=zb, zt_end=ze)

  #print(f"Summ Block_2  {Tb2} !! {Te2}  X= {x_data2} #  Y= {y_values2}")

  if not p2:
    for i in range(len(y_values2)):
      if y_values2[i][2]:  #
        bp_summary2.append({"date": y_values2[i][1], "sys": y_values2[i][2], "dia": y_values2[i][3], \
                           "pul": y_values2[i][4], "mean": y_values2[i][5], "afib": y_values2[i][6]})

  # prep data Block 1
  р1, x_data, y_values = anvil.server.call("prep_plot", object, Tb=Tb1, Te=Te1, Step=Step,
                                           Average=True, zt_beg=zb, zt_end=ze)
  #print(f"Summ Block_1  {Tb1} !! {Te1}  X= {x_data} #  Y= {y_values}")
  if not p1:
    for i in range(len(y_values)):
      if y_values[i][2]:  #
        bp_summary.append({"date": y_values[i][1], "sys": y_values[i][2], "dia": y_values[i][3], \
                           "pul": y_values[i][4], "mean": y_values[i][5], "afib": y_values[i][6]})
  if p2 or p1:
    # Data prep error
    m = f"set_summary() p2= {p2}  p1= {p1}"
    anvil.server.call("mh_log", -902, m)
    return(-902)

  # Generate comp_summary  #[{"no", "s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}] 
  for i in range(len(bp_summary)):
    if all or bp_summary[i]["date"]:
      comp_summary.append({"no": "AVRG", "s1":bp_summary[i]["sys"], "s2":bp_summary2[i]["sys"], "d1":bp_summary[i]["dia"],
                        "d2":bp_summary2[i]["dia"], "p1":bp_summary[i]["pul"], "p2":bp_summary2[i]["pul"],"m1":bp_summary[i]["mean"],
                        "m2":bp_summary2[i]["mean"], "a1":bp_summary[i]["afib"], "a2":bp_summary2[i]["afib"]})

  
  # MAX row   MAX(sys), MAX(dia), MAX(pul), MAX(mean), MAX(afib)
  # max_row1=[]; min_row1=[]; max_row2=[]; min_row2=[]
  p1, max_row1, min_row1 = anvil.server.call("get_max_min", object, Tb1, Te1, zt_beg=zb, zt_end=ze)
  p2, max_row2, min_row2 = anvil.server.call("get_max_min", object, Tb2, Te2, zt_beg=zb, zt_end=ze)
  if p2 or p1:
    # Data prep error
    m = f"set_comp_summary() p2= {p2}  p1= {p1}"
    anvil.server.call("mh_log", -903, m)
  
  max_row = {"no":"MAX", "s1": None, "s2": None, "d1": None, "d2": None, 
             "p1": None, "p2": None, "m1": None, "m2": None, "a1": None, "a2": None}
  max_row["s1"] = max_row1[0]; max_row["s2"] = max_row2[0]
  max_row["d1"] = max_row1[1]; max_row["d2"] = max_row2[1]
  max_row["p1"] = max_row1[2]; max_row["p2"] = max_row2[2]
  max_row["m1"] = max_row1[3]; max_row["m2"] = max_row2[3]
  max_row["a1"] = max_row1[4]; max_row["a2"] = max_row2[4]

  # MIN row
  min_row = {"no": "MIN", "s1": None, "s2": None, "d1": None, "d2": None,
            "p1": None, "p2": None, "m1": None, "m2": None, "a1": None, "a2": None}                      
  min_row["s1"] = min_row1[0]; min_row["s2"] = min_row2[0]
  min_row["d1"] = min_row1[1]; min_row["d2"] = min_row2[1]
  min_row["p1"] = min_row1[2]; min_row["p2"] = min_row2[2]
  min_row["m1"] = min_row1[3]; min_row["m2"] = min_row2[3]
  min_row["a1"] = min_row1[4]; min_row["a2"] = min_row2[4]

  comp_summary.append(max_row)
  comp_summary.append(min_row)
  
  return (0)
