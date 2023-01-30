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

x_data = []
y_values = []

def set_bp_list():
  global x_data  # !! Иначе не прехвърля данните (за разлика от променливите, работещи с appens)
  global y_values
  # Retreive data from DB
  r, x_data, y_values = anvil.server.call("prep_data", "1001", "2021/07/22 00:00", "2021/08/23 23:59",\
                                1440, fill_empty=False)
  #data format: ["          ", "                ", (s); (d); (p); (m); (a)]
  #print(y_values)
  #print(x_data)
  if not r:
    all = False    # all - including records without values (measurements)
    for i in range(len(y_values)):
      if all or y_values[i][2]:    # y_values[i][2] / True
        bp_list.append({"date": y_values[i][1], "sys":y_values[i][2], "dia":y_values[i][3], "pul":y_values[i][4], "mean":y_values[i][5], "afib":y_values[i][6]})    # x_data[i]
        # {"date": bp_dat[0], "sys":bp_sys[0], "dia":bp_dia[0], "pul":bp_pul[0], "mean":bp_mea[0], "n":bp_n[0]}
        bp_dia.append(y_values[i][3])        
        bp_sys_add.append(y_values[i][2] - y_values[i][3])
        if y_values[i][2] >= 140 or y_values[i][3] >= 90:
          bp_colors.append("rgba(255,0,0, 0.8)")        
        elif y_values[i][2] >= 135 or y_values[i][3] >= 85:
          bp_colors.append("rgba(245,195,39, 0.8)")
        else:
          bp_colors.append("rgba(0,255,0, 0.8)")
        
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



def get_data():
  r, x_data, y_values = anvil.server.call("prep_data", "1001", "2022/04/09 00:00", "2022/04/12 23:59",\
                                360, fill_empty=False)


'''   TEST SET
bp_dat = ["01/01 11:12", "02/01 22:22", "03/01 22:23", "04/01 22:24", "05/01 22:25", "06/01 22:26",
         "07/01 22:30", "08/01 07:30", "09/01 0933", "10/01 08:50"]
bp_sys = [142, 135, 134, 122, 138, 118, 115, 142, 135, 134]
bp_dia = [90, 85, 85, 78, 82, 75, 79, 90, 85, 85,]
bp_sys_add = []
bp_pul = [160, 61, 62, 63, 64, 65, 66, 67, 68, 69]
bp_mea = [100, 101, 102, 103, 104, 105, 88, 89, 80, 79]
bp_n = [120, 21, 22, 23, 24, 25, 26, 27, 28, 29]
bp_list = []

def set_bp_list():
  for i in range(10):
    bp_list.append({"date": bp_dat[i], "sys":bp_sys[i], "dia":bp_dia[i], "pul":bp_pul[i], "mean":bp_mea[i], "n":bp_n[i]})
    # {"date": bp_dat[0], "sys":bp_sys[0], "dia":bp_dia[0], "pul":bp_pul[0], "mean":bp_mea[0], "n":bp_n[0]}
    bp_sys_add.append(bp_sys[i] - bp_dia[i])
''' 