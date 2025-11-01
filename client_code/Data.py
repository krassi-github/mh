import datetime
import anvil.server
#    from . import Module1

# LOCAL Data Layer

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
slice_mode = False  # on True Daily Data is sliced
slice_step = None   # Slice step (time) in hours

# filter_a (Analysis Form) Data
uom_items = [('Day', "d"), ("Week", "w"), ("30days", "m")]    # ("Month", "m") 09-10-2025
uom = ''
max_number = (99, )   # max value of number (in period length)
number = 0            # period = uom * number 
step = 0
Tb1 = ""              # beg times & end times for comparative analysis
Tb2 = ""
Te1 = ""
Te2 = ""

time_from = ""        # for range operartions; governed from Filter; initially set from load_params
time_to = ""         #
current_date = ""     # 
current_range = ''
loaded_from = ""    
loaded_to = ""
loaded_from2 = ""      # second BP set for comparison
loaded_to2 = ""

comp_list = []    #[{"n", "no", "date2", " s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}]
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

bp_list = []     # main data list [{}] # "date", "SYS", "DIA", "PUL", "MEA", "afib"
bp_summary = []  # summary
x_data = []      # time data (X axis)
y_values = []    # blood pressure values
afibs = []
# Slice mode related
afibs_dt_cnt = [] # [{dt: yyyy/mm/dd hh:hh, cnt: int}] # Its length = number of steps with afib events in the range
                  # filled by first block of set_bp_list() (regular mode); used by second block (slice_mode)
# color_counters (correspond to BP ranges)
purple_cntr = 0  
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
bp_list2 = []     # main data list [{}]  # "date", "SYS", "DIA", "PUL", "MEA", "afib"
bp_summary2 = []  # summary
afibs2 = []       # afib events
x_data2 = []      # time data (X axis)
y_values2 = []    # blood pressure values
purple_cntr2 = 0  # color_counters (correspond to BP ranges)
red_cntr2 = 0     
orange_cntr2 = 0
green_cntr2 = 0

# ******************************************************************************
# Load parameters funcs
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


# MIX
def comp_list_export():
  global comp_list
  
  return(anvil.server.call("comp_list_export", comp_list))


# *************************************************************************************    
# Load Data Funcs

# Aux func - filters records, whose dt.hour is within slice_window out of afibs_dt_cnt
def get_afibs_in_slice_hhmm(zb_str, ze_str, dt):
  """
  Филтрира afibs_dt_cnt по часовия слайс.
  zb_str, ze_str : низове 'HH:MM'
  afibs_dt_cnt   : list['YYYY/MM/DD HH:MM']
  Връща всички записи, чийто час попада в [zb, ze),
  като работи и при слайс, който пресича 00:00.
  """
  # парсваме границите
  zb = datetime.datetime.strptime(zb_str, "%H:%M").time()
  ze = datetime.datetime.strptime(ze_str, "%H:%M").time()

  results = []
  for rec in dt:
    # извличаме часовата част от низа 'YYYY/MM/DD HH:MM'
    try:
      dt_time = datetime.datetime.strptime(rec, "%Y/%m/%d %H:%M").time()
    except Exception:
      print(f"Wrong format EXCEPTION rec= {rec}")
      continue  # пропускаме лош формат
    # стандартен или "wrap-around" слайс (примерно 22:00–02:00)
    if zb <= ze:
      in_slice = zb <= dt_time < ze
    else:
      in_slice = (dt_time >= zb) or (dt_time < ze)
    if in_slice:
      results.append(rec)
  return results


# set_bp_list()  ----------------------------------------------------------------------
# Data Block 1 filled
def set_bp_list(user_id, fr=None, Tb=None, Te=None, Step=None, crawl=False, fill_empty=None):    
  global current_date, all
  global x_data, y_values
  global params, current_range
  global bp_list, bp_date, bp_sys, bp_dia, bp_pul, bp_sys_add, bp_mean, bp_afib
  global afibs_date, afibs_dt_cnt
  global bp_colors,  purple_cntr, red_cntr, orange_cntr, green_cntr
  global loaded_from      # loaded data time stamp FROM (x_data[0]])
  global loaded_to        # loaded data time stamp TO   (x_data[-1])
  global zt_beg           # beg of time zone
  global zt_end           # end of time zone

  # 20-06-2025  current_date and fr signal to prep_plot() that work range will be different from last_date !!!
  # tb = current_date + " 00:00" if fr and fr != 'r' and current_date else Tb    # tb is replace of Tb for prep_plt() calla !!

  # Regular retreive
  if zt_beg == "00:00" and zt_end == "23:59":
    zb = None
    ze = None
  else:
    zb = zt_beg
    ze = zt_end
  r, x_data, y_values = anvil.server.call("prep_plot", user_id, fr=fr, Tb=Tb, Te=Te, Step=Step, \
                                          Average=False, fill_empty=fill_empty,
                                          crawl=crawl, zt_beg=zb, zt_end=ze, cur_date=current_date)
  if x_data and r > 0:
    # data is available
    loaded_from = x_data[0]     # test x_data alternatively
    loaded_to = x_data[-1]
      
  bp_list = []      # "date", "SYS", "DIA", "PUL", "MEA", "afib"
  bp_date = []; bp_sys = []; bp_dia = []; bp_pul = []; bp_sys_add = []; bp_mean = []; bp_afib = []
  bp_colors = []; green_cntr = 0; orange_cntr = 0; red_cntr = 0; purple_cntr = 0; afibs_dt_cnt = []
  
  if r >= 0:       
    for i in range(len(y_values)):      
      if all or y_values[i][2]:    #  
        # AII (AFIB Intensity Index) calc all but 'd'and 'w' foxed ranges  31-10-2025
        afib_data = [{"aii": ''}]
        if fr not in ('d', 'w') and y_values[i][6] not in (None, ""):
          afib_data = anvil.server.call(
            "get_afib_yearly_summary",
            date_from=x_data[i],	                #date_from,
            date_to=x_data[i+1],                   #date_to,
            zt_beg=zt_beg,
            zt_end=zt_end
          )
        
        bp_list.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6], "aii":afib_data[0]["aii"] })        
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
          if y_values[i][2] > 0:
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

        if y_values[i][6]:  # AFIB -------------
          bp_afib.append(y_values[i][6])
        else:
          bp_afib.append(None)

  if slice_mode:  # SLICE mode ------------------------------
    x_data = []
    y_values = []
    bp_list = []

    ii = 0  # loop counter on slice windows
    for z in range(0, 24, slice_step):
      zb = str(z).zfill(2) + ":00"      # the time zone beginning
      zb2 = str(z).zfill(2) + ":00"     # the time zone beginning COPY
      hr = z + slice_step
      if hr == 24:
        ze = "23:59"
      else:
        ze = str(hr).zfill(2) + ":00"
      # Retreive a single record (the summary) for the range of slice window
      r, x_dat, y_val = anvil.server.call("prep_plot", user_id, fr=fr, Tb=Tb, Te=Te, Step=Step, \
                                          Average=True, fill_empty=fill_empty,
                                          crawl=crawl, zt_beg=zb, zt_end=ze, cur_date=current_date)     
      # ToDo Processing on r= no data !!

      # prep data for the Slice modee -------------------
      _dt   = y_val[0][1].strip()
      #if _dt and _dt[:4] != "2025":
      #  print(f"DateException {_dt} fr= {fr} Tb= {Tb} Te= {Te} sl= {zb + '-' + ze}  {y_val}")
      _afib = y_val[0][6]
      if _afib:
        _cnt = 1 if _afib == "AFIB" else int(_afib[:-2])
      else:
        _cnt = 0
      sl = zb + '-' + ze    # to get the date of this record (first in slice window)

      if _dt and _afib:
        r, slice_afibs = anvil.server.call("get_afibs", _dt, number=1, slice_window=sl)      
        if len(slice_afibs): 
          afibs_dt_cnt.append({"dt": slice_afibs[0][0], "cnt": _cnt})  # date_time of afib
          #print(f"{slice_afibs[0][0]} _dt= {_dt}  _afib= {_afib}  {slice_afibs}")
        else:
          afibs_dt_cnt.append({"dt": '', "cnt": 0})
      else:
        afibs_dt_cnt.append({"dt": '', "cnt": 0})
      y_val[0][1] = zb + " - " + (str(z + slice_step).zfill(2) + ":00")    # form the slice frame for data grid
      zb = str(x_dat[0][:10]) + ' ' + zb
      y_values.extend(y_val)    # append ? changed on the recovery process
      x_data.append(zb)
      ii += 1
    
    for i in range(len(y_values)):      
      if all or y_values[i][2] or slice_mode:    # za filtrirane na redowe bez izmerwaniq
        #                         slice_mode added 26-10-2025 ==> fill up full slices set if necessary
        # AII (AFIB Intensity Index) calc all but 'd'and 'w' foxed ranges  31-10-2025
        afib_data = [{"aii": ''}]
        if fr not in ('d', 'w') and y_values[i][6] not in (None, ""):
          if len(x_data) <= i:
            print(f"i= {i} L= {len(x_data)} {x_data}")
          afib_data = anvil.server.call(
            "get_afib_yearly_summary",
            date_from=x_data[i],	                #date_from,
            date_to=x_data[i+1],                   #date_to,
            zt_beg=zt_beg,
            zt_end=zt_end
          )
          
        bp_list.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6], "aii":afib_data[0]["aii"]})     

    loaded_from = str(x_data[0])
    loaded_to = str(x_dat[-1][:10]) + ' ' + ze  
    # print(f"afibs_dt_cnt {afibs_dt_cnt}")
  return(r)
  
# -------------------------------------------------------------------------------------------------------------------------------
def set_summary(user_id, fr=None, Tb=None, Te=None, crawl=False):
  global current_date
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
                        Tb=Tb, Te=Te, Average=True, fill_empty=False, crawl=crawl, 
                                          zt_beg=zb, zt_end=ze, cur_date=current_date) # 21-06-2025  cur_date
  # ======= print(f"Summ  {Tb} !! {Te}  X= {x_data} #  Y= {y_values}")
  if r >= 0:       
    for i in range(len(y_values)):      
      if y_values[i][2]:    #        
        bp_summary.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3],\
                        "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})
  return(r)

# --------------------------------------------------------------------------------------------------------
def afib_details(row_date, L1=None, L2=None, slice_window=None):
  # L1 Link to the period 1 of analysis (Basic List to be used)
  # L2 Link to the period 2 of analysis (List 2 to be used)
  global bp_list, bp_list2, slice_mode, afibs, afibs_dt_
  bp_ = bp_list2 if L2 else bp_list
  if L2:
    row_date = L2

  rows_out = []
  if row_date != "":    # "**"
    if not slice_mode:
      for b in bp_:
        if b['date'] == row_date:    #  or slice_mode 25-10-2025
          a = b.get('afib')
          if a:
            afib_value = 1 if a == "AFIB" else int(a[:-2])
            #print(f"row_date= {row_date} a= {a} afib_value= {afib_value}")    #  afibs_date= {afibs_date}
            _, rows = anvil.server.call("get_afibs", row_date, number=afib_value, slice_window=slice_window )
    else:   
      match = next((rec for rec in afibs_dt_cnt if rec.get("dt") == row_date), None)      
      if match:
        afib_dt = match["dt"]
        afib_value = match["cnt"]
        _, rows = anvil.server.call("get_afibs", afib_dt, number=afib_value, slice_window=slice_window)
      else:
        afib_dt = None
        afib_cnt = 0
        rows = []
            
    for r in rows:
      rows_out.append({
        "date": r[0],
        "sys": r[1],
        "dia": r[2],
        "pul": r[3],
        "mean": r[4]
      })
  afibs = rows_out
  msg = "" if rows_out else "No AFIB for this row "
  return rows_out, msg


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
  if p2 < 0 or p1 < 0:
    # Data prep error
    m = f"set_comp_list() p2= {p2}  p1= {p1}"
    anvil.server.call("mh_log", -901, m)
    return(-901)

  # Generate comp_list  #[{"n", "no", "date2", "s1", "s2", "d1", "d2", "p1", "p2", "m1", "m2", "a1", "a2"}]
  len1= len(y_values);  len2= len(y_values2)
  if len1 >= len2:
    min_len = len2    # len2-1  23-12-2023 gonene na comp_list (len = 0)
  else:
    min_len = len1    # len1-1
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


# AFIB yearly summary
def afibs_year_summary(year: str):
  global time_from, time_to, zt_beg, zt_end
  # return [{'year': 2025, 'N_measurements': 2450, 'S_afib_units': 13, 'AII': 0.005306, 'AFIB_minutes': 16.25}]
  if year == "all":
    
    afibs_data = anvil.server.call(
      "get_afib_yearly_summary",
      date_from="2021/01/01",	                #date_from,
      date_to="2025/12/31",                   #date_to,
      zt_beg=zt_beg,
      zt_end=zt_end
    )
  return (afibs_data)
