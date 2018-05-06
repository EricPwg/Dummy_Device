from threading import Thread
import time, DAN, requests, random

import tkinter as tk

ServerIP = '140.113.199.199' #Change to your IoTtalk IP or None for autoSearching
Reg_addr = None #None # if None, Reg_addr = MAC address

idf_List = ['CO2 Plantbox', 'O2 Plantbox', 'Humidity Plantbox', 'Temperature Plantbox', 'Watching Dog', 'Water Level Plantbox']
odf_List = ['LED1 Plantbox',  'LED2 Plantbox', 'LED3 Plantbox', 'Moter1 Plantbox', 'Moter2 Plantbox', 'Moter3 Plantbox']
dan_List = list(idf_List)
dan_List.extend(odf_List)

DAN.profile['dm_name']='Plantbox'
DAN.profile['df_list']=dan_List
DAN.profile['d_name']= 'Dummy_Plantbox' # None for autoNaming
DAN.device_registration_with_retry(ServerIP, Reg_addr)

'''
while True:
    try:
        for i in range(6):
            value2=random.uniform(1, 10)
            DAN.push (DAN.profile['df_list'][i], value2)
            
    #Pull data from a device feature called "Dummy_Control"
        value1=DAN.pull('Dummy_Control')
        if value1 != None:
            print (value1[0])

    #Push data to a device feature called "Dummy_Sensor"
        value2=random.uniform(1, 10)
        DAN.push ('Dummy_Sensor', value2)
        
    except Exception as e:
        print(e)
        DAN.device_registration_with_retry(ServerIP, Reg_addr)

    time.sleep(0.2)
'''

def handle_push(idf_index, value):
    DAN.push(idf_List[idf_index], value)
    time.sleep(0.1)
    print('Push: {0} = {1}'.format(idf_List[idf_index], value))
    
'''
function_List = []
for i in range(len(idf_List)):
    fn = lambda v: handle_push(idf_List[i], v)
    function_List.append(fn)
'''

idf_min = [400, 15, 5, 10, 0, 0]
idf_max = [800, 30, 80, 35, 1, 1023]
idf_res = [10, 0.5, 0.5, 0.5, 1, 2]

def push0(v):
    handle_push(0, v)
def push1(v):
    handle_push(1, v)
def push2(v):
    handle_push(2, v)
def push3(v):
    handle_push(3, v)
def push4(v):
    handle_push(4, v)
def push5(v):
    handle_push(5, v)

function_List = [push0, push1, push2, push3, push4, push5]

win = tk.Tk()
win.title('Dummy Plantbox')

tk.Label(win, width = 40, height = 2, bg = 'gray', font = ('Arial', 12), text = 'IoTtalk Server = http://'+ServerIP+':9999').grid(row = 0, column = 0, columnspan = 2)
tk.Label(win, width = 40, height = 2, bg = 'gray', font = ('Arial', 12), text = 'Device name = '+DAN.profile['d_name']).grid(row = 1, column = 0, columnspan = 2)

row_offset = 2
for i in range(len(idf_List)):
    l = tk.Label(win, width = 20, text = idf_List[i]).grid(row = i+row_offset, column = 0)
    tk.Scale(win, orient=tk.HORIZONTAL, from_=idf_min[i], to=idf_max[i], resolution=idf_res[i], length=600, tickinterval=int((idf_max[i]-idf_min[i])/10), command = function_List[i]).grid(row = i+row_offset, column = 1)

row_offset = 8
Label_List = []
for i in range(len(odf_List)):
    tk.Label(win, width = 20, text = odf_List[i]+':').grid(row = row_offset+i, column = 0)
    l = tk.Label(win, text = ' ')
    l.grid(row = row_offset+i, column = 1)
    Label_List.append(l)


#l1 = tk.Label(win, text = 'LED1').grid(row = 8, column = 0)
#l2 = tk.Label(win, text = '').grid(row = 8, column = 1)

live_flag = True

def whilepull():
    global Label_List
    while live_flag:
        for i in range(len(odf_List)):
            value = DAN.pull(odf_List[i])
            #print('Pull: {0} = {1}'.format(odf_List[i], value))
            if value != None:
                print('Pull: {0} = {1}'.format(odf_List[i], value[0]))
                Label_List[i].config(text = str(value[0]))
        time.sleep(1)

def end_program():
    global live_flag
    live_flag = False
    win.destroy()

b = tk.Button(win, text = 'Exit', command = end_program).grid(row = 14, column = 0, columnspan = 2)

t_bao2 = Thread(target=whilepull)
t_bao2.daemon = True
t_bao2.start()

#s = tk.Scale(win, label = 'test', command = fn).grid(row = 2, column = 1)

win.mainloop()