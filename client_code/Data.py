# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
bp_dat = ["01/01 11:12", "02/01 22:22", "03/01 22:23", "04/01 22:24", "05/01 22:25", "06/01 22:26" ]
bp_sys = [142, 135, 134, 122, 138, 118]
bp_dia = [90, 85, 85, 78, 82, 75]
bp_pul = [60, 61, 62, 63, 64, 65]
bp_mea = [100, 101, 102, 103, 104, 105]
bp_n = [20, 21, 22, 23, 24, 25]
bp_list = []
#[lambda x: for i in range(5): ({"date": bp_dat[i], "sys":bp_sys[i], "dia":bp_dia[i], "pul":bp_pul[i], "mean":bp_mea[i], "n":bp_n[i]}]

def set_bp_list():
  for i in range(6):
    bp_list.append({"date": bp_dat[i], "sys":bp_sys[i], "dia":bp_dia[i], "pul":bp_pul[i], "mean":bp_mea[i], "n":bp_n[i]})
    # {"date": bp_dat[0], "sys":bp_sys[0], "dia":bp_dia[0], "pul":bp_pul[0], "mean":bp_mea[0], "n":bp_n[0]}


