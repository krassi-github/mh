import anvil.server
#    from . import Module1
#    Module1.say_hello()
#import sqlite3

bp_dat = ["01/01 11:12", "02/01 22:22", "03/01 22:23", "04/01 22:24", "05/01 22:25", "06/01 22:26",
         "07/01 22:30", "08/01 07:30", "09/01 0933", "10/01 08:50"]
bp_sys = [142, 135, 134, 122, 138, 118, 115, 142, 135, 134]
bp_dia = [90, 85, 85, 78, 82, 75, 79, 90, 85, 85,]
bp_sys_add = []
bp_pul = [160, 61, 62, 63, 64, 65, 66, 67, 68, 69]
bp_mea = [100, 101, 102, 103, 104, 105, 88, 89, 80, 79]
bp_n = [120, 21, 22, 23, 24, 25, 26, 27, 28, 29]
bp_list = []
#[lambda x: for i in range(5): ({"date": bp_dat[i], "sys":bp_sys[i], "dia":bp_dia[i], "pul":bp_pul[i], "mean":bp_mea[i], "n":bp_n[i]}]

def set_bp_list():
  for i in range(10):
    bp_list.append({"date": bp_dat[i], "sys":bp_sys[i], "dia":bp_dia[i], "pul":bp_pul[i], "mean":bp_mea[i], "n":bp_n[i]})
    # {"date": bp_dat[0], "sys":bp_sys[0], "dia":bp_dia[0], "pul":bp_pul[0], "mean":bp_mea[0], "n":bp_n[0]}
    bp_sys_add.append(bp_sys[i] - bp_dia[i])
    
# ===============================================================================================================================
# Retreive data from DB
x_data = []
y_values = []

def get_data():
  r, x_data, y_values = anvil.server.call("prep_data", "1001", "2022/04/09 00:00", "2022/04/12 23:59",\
                                360, fill_empty=False)

