from logging import exception
import re
import threading
import time
import json
from collections import OrderedDict
from turtle import title
import pyautogui
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
import keyboard
from tkinter import END, messagebox
from tkinter import filedialog

window = tk.Tk()
window.title('Tnank you for your help')
window.geometry('1000x400+0+0')
window.resizable(True,True)

font_15 = font.Font(size=15)
font_15_bold = font.Font(size=15, weight='bold')

select_func_list = ['Mouse', 'Keyboard', 'Hotkey', 'Write' 'Text']
mouse_func_list = ['L-Click', 'L-Down', 'L-Up', 'R-Click', 'R-Down', 'R-Up', 'L-Double','L-Triple', 'Move', 'Drag']
key_func_list = ['Press', 'KeyDown', 'KeyUp']
key_list = ['left', 'right', 'up', 'down','enter', 'esc', 'escape', 'space', 'backspace', 'tab', 'alt', 'altleft', 'altright', 'ctrl', 'ctrlleft', 'ctrlright', 'shift', 'shiftleft', 'shiftright', 'del', 'delete', 'end', 'hanguel', 'hangul', 'home', 'insert',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
            'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'printscreen', 'prntscrn', 'scrolllock',
            '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',  ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
            'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7','8', '9',
            'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock'
            ]
hotkey_list = ['Ctrl+a', 'Ctrl+c', 'Ctrl+v']

save_condition_arr=[]       #save all things, [num, act_deact, select_func, mouse_func, mouseX, mouseY, key_func, key_combo, hotkey, text_ent, delay_ent, target_win_posX, target_win_posY]

t_cnt=0                     #total target window number
target_win_arr=[]           #save target windows
target_lb1_arr=[]           #target number label
target_lb2_arr=[]           #'+' label 
act_chk_btn_arr=[]          #act/deactive check box 
chk_var=[]                  #save checked or not(1 or 0) for act_chk_btn
no_lb_arr=[]                #number of list
select_func_combo_arr=[]    #select function(mouse, keyboard, hotkey, text)
mouse_func_combo_arr=[]     #mouse function
key_func_combo_arr=[]
key_combo_arr=[]
hotkey_combo_arr=[]
text_entry_arr=[]
delay_entry_arr=[]

thd1_bool = False           #thread boolean

#make new target window
def makeTarget(act_deact = 1, select_func=0, mouse_func=0, key_func=0, key_combo=0, hotkey=0, text_ent='', delay_ent='1000', target_win_posX='0', target_win_posY='0'):
    t_cnt = len(target_win_arr)
    #make new window and setting
    target_win_arr.append(tk.Toplevel(window))
    target_win_arr[t_cnt].wm_attributes("-topmost", True)
    target_win_arr[t_cnt].wm_attributes("-transparentcolor", '#F0F0F0')      #to make window transparent
    target_win_arr[t_cnt].geometry('150x100' + '+' + target_win_posX + '+' + target_win_posY)
    target_win_arr[t_cnt].overrideredirect(True)

    #show target num and target point '+'
    target_lb1_arr.append(tk.Label(target_win_arr[t_cnt], borderwidth=1, relief='ridge', bg='red', text=str(t_cnt+1)))
    target_lb2_arr.append(tk.Label(target_win_arr[t_cnt], borderwidth=1, relief='ridge', width=3, font=font_15, fg='red', text='+'))
    target_lb1_arr[t_cnt].grid(row=0, column=0,sticky='ns')
    target_lb2_arr[t_cnt].grid(row=0, column=1)    

    #create checkbutton, label, combobox, entry
    chk_var.append(tk.IntVar())
    no_lb_arr               .append(tk.Label(set_target_lbframe, text=str(t_cnt+1)))
    act_chk_btn_arr         .append(ttk.Checkbutton(set_target_lbframe, variable=chk_var[t_cnt]))
    select_func_combo_arr   .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=select_func_list))
    mouse_func_combo_arr    .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=mouse_func_list))
    key_func_combo_arr      .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=key_func_list))
    key_combo_arr           .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=key_list))
    hotkey_combo_arr        .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=hotkey_list))
    text_entry_arr          .append(tk.Entry(set_target_lbframe))
    delay_entry_arr         .append(tk.Entry(set_target_lbframe, justify='right', width=8))

    #grid checkbutton, label, combobox, entry
    no_lb_arr               [t_cnt].grid(row=t_cnt+2, column=0, padx=(5,5), pady=(5,0))
    act_chk_btn_arr         [t_cnt].grid(row=t_cnt+2, column=2, padx=(5,5), pady=(5,0))
    select_func_combo_arr   [t_cnt].grid(row=t_cnt+2, column=4, padx=(5,5), pady=(5,0))
    mouse_func_combo_arr    [t_cnt].grid(row=t_cnt+2, column=6, padx=(5,5), pady=(5,0))
    key_func_combo_arr      [t_cnt].grid(row=t_cnt+2, column=8, padx=(5,5), pady=(5,0))
    key_combo_arr           [t_cnt].grid(row=t_cnt+2, column=10, padx=(5,5), pady=(5,0))
    hotkey_combo_arr        [t_cnt].grid(row=t_cnt+2, column=12, padx=(5,5), pady=(5,0))
    text_entry_arr          [t_cnt].grid(row=t_cnt+2, column=14, padx=(5,5), pady=(5,0))
    delay_entry_arr         [t_cnt].grid(row=t_cnt+2, column=16, padx=(5,5), pady=(5,0))

    chk_var                 [t_cnt].set(act_deact)              #always checked when it created
    select_func_combo_arr   [t_cnt].current(select_func)        #select first value
    mouse_func_combo_arr    [t_cnt].current(mouse_func)         #select first value
    key_func_combo_arr      [t_cnt].current(key_func)           #select first value
    key_combo_arr           [t_cnt].current(key_combo)          #select first value
    hotkey_combo_arr        [t_cnt].current(hotkey)             #select first value
    text_entry_arr          [t_cnt].delete(0, tk.END)
    text_entry_arr          [t_cnt].insert(0, text_ent)
    delay_entry_arr         [t_cnt].delete(0, tk.END)
    delay_entry_arr         [t_cnt].insert(0, delay_ent)
    actDeactWidgets('')

    #to move target point using mouse drag
    def drag(event):
        if(not(thd1_bool)):
            width = str(target_win_arr[t_cnt].winfo_width())
            height = str(target_win_arr[t_cnt].winfo_height())
            pos_x = str(pyautogui.position().x)
            pos_y = str(pyautogui.position().y)
            target_win_arr[t_cnt].geometry(width + 'x' + height + '+' + pos_x + '+' + pos_y)

    #mouse left drag event
    target_win_arr[t_cnt].bind("<B1-Motion>", drag)
    #only digit input
    delay_entry_arr[t_cnt].bind('<KeyRelease>', onlyNumbers)
    #when combobox selected, widget condition will be change 
    select_func_combo_arr[t_cnt].bind('<<ComboboxSelected>>', actDeactWidgets)
    #refresh scrollbox when item added
    canvas.configure(scrollregion=canvas.bbox("all"))

#delete target and list
def delTarget():
    t_cnt = len(target_win_arr)
    if t_cnt != 0:
        #destroy widgets
        target_lb1_arr          [t_cnt-1].destroy()
        target_lb2_arr          [t_cnt-1].destroy()
        target_win_arr          [t_cnt-1].destroy()
        act_chk_btn_arr         [t_cnt-1].destroy()
        no_lb_arr               [t_cnt-1].destroy() 
        select_func_combo_arr   [t_cnt-1].destroy()
        mouse_func_combo_arr    [t_cnt-1].destroy()
        key_func_combo_arr      [t_cnt-1].destroy()
        key_combo_arr           [t_cnt-1].destroy()
        hotkey_combo_arr        [t_cnt-1].destroy()
        text_entry_arr          [t_cnt-1].destroy()
        delay_entry_arr         [t_cnt-1].destroy()

        #remove list
        target_lb1_arr          .pop()
        target_lb2_arr          .pop()
        target_win_arr          .pop()
        act_chk_btn_arr         .pop()
        no_lb_arr               .pop() 
        select_func_combo_arr   .pop()
        mouse_func_combo_arr    .pop()
        key_func_combo_arr      .pop()
        key_combo_arr           .pop()
        hotkey_combo_arr        .pop()
        text_entry_arr          .pop()
        delay_entry_arr         .pop()
        chk_var                 .pop()
    else:
        print('no widget to delete')

    #refresh scrollbox when item deleted
    canvas.configure(scrollregion=canvas.bbox("all"))

#thread start
def threadStart():
    global thd1_bool
    thd1 = threading.Thread(target=saveCondition)
    if(thd1_bool):
        print('already thread started.')
        thd1_bool = False
    else:
        if(len(target_win_arr) < 1):
            messagebox.showwarning(title='Warning', message='Please add targets push the + button')
        else:
            print('thread start!')
            thd1_bool = True
            start_btn.config(bg='red')
            thd1.start()
            

#thread stop
def threadStop():
    global thd1_bool
    thd1_bool = False

#check incorrect values
def checkValues():
    loop = loop_entry.get()
    init_delay = init_delay_entry.get()

    #init delay empty check
    if(init_delay == ''):
        init_delay_entry.insert(0,'1000')

    #Loop empty check
    if(loop == ''):
        loop_entry.insert(0,'1')

    #delay empty check
    t_cnt = len(target_win_arr)
    for idx in range(0, t_cnt):
        delay_ent   = delay_entry_arr[idx].get()
        if(delay_ent == ''):
            delay_entry_arr[idx].insert(0,'10')
     


#when you push the start button, it will save target points and ect. only act checked
def saveCondition():
    try:
        checkValues()
        allWidgetsActDeact()
        
        save_condition_arr.clear()
        t_cnt = len(target_win_arr)
        for idx in range(0, t_cnt):
            num             = no_lb_arr[idx].cget('text')
            act_deact       = chk_var[idx].get()
            select_func     = select_func_combo_arr[idx].get()
            mouse_func      = mouse_func_combo_arr[idx].get()
            #mouse target point X,Y
            mouseX          = target_lb2_arr[idx].winfo_rootx() + (target_lb2_arr[idx].winfo_width())/2
            mouseY          = target_lb2_arr[idx].winfo_rooty() + (target_lb2_arr[idx].winfo_height())/2
            key_func        = key_func_combo_arr[idx].get()
            key_combo       = key_combo_arr[idx].get()
            hotkey          = hotkey_combo_arr[idx].get()
            text_ent        = text_entry_arr[idx].get()
            delay_ent       = delay_entry_arr[idx].get()
            delay_ent       = int(delay_ent) / 1000
            target_win_posX = str(target_win_arr[idx].winfo_rootx())
            target_win_posY = str(target_win_arr[idx].winfo_rooty())

            save_condition_arr.append([num, act_deact, select_func, mouse_func, mouseX, mouseY, key_func, key_combo, hotkey, text_ent, delay_ent, target_win_posX, target_win_posY])
            
        for item in save_condition_arr:
            print(item)

        if(thd1_bool):
            play()

    except Exception as e:
        print('play error : ',e)


def targetCrossActDeact(show):
    if(show):
        cnt = len(target_lb2_arr)
        for idx_lb in range(0, cnt):
            target_lb2_arr[idx_lb]['text']='+'
    else:
        cnt = len(target_lb2_arr)
        for idx_lb in range(0, cnt):
            target_lb2_arr[idx_lb]['text']=''


def play():
    global thd1_bool
    targetCrossActDeact(False)

    loop = loop_entry.get()
    init_delay = init_delay_entry.get()
    loop = int(loop)

    #init delay
    init_delay = int(init_delay_entry.get()) /1000
    time.sleep(init_delay)

    for idx_lp in range(1, loop+1):
        #show loop progress
        prog_loop_lb2.config(text=str(idx_lp).zfill(3) + '/' + str(loop).zfill(3))
        for idx, item in enumerate(save_condition_arr):
            if(thd1_bool == False): break
            #show loop progress
            prog_element_lb2.config(text=str(idx+1).zfill(3) + '/' + str(len(save_condition_arr)).zfill(3))
            if(item[1] == 1):   #act_chkbtn is checked
                if(item[2] == 'Mouse'):
                    if(item[3] == 'L-Click'):
                        pyautogui.click(button='left', x=item[4], y=item[5])
                    elif(item[3] == 'L-Down'):
                        pyautogui.mouseDown(button='left', x=item[4], y=item[5])
                    elif(item[3] == 'L-Up'):
                        pyautogui.mouseUp(button='left', x=item[4], y=item[5])
                    elif(item[3] == 'R-Click'):
                        pyautogui.click(button='right', x=item[4], y=item[5])
                    elif(item[3] == 'R-Down'):
                        pyautogui.mouseDown(button='right', x=item[4], y=item[5])
                    elif(item[3] == 'R-Up'):
                        pyautogui.mouseUp(button='right', x=item[4], y=item[5])
                    elif(item[3] == 'L-Double'):
                        pyautogui.click(clicks=2, button='left', x=item[4], y=item[5])
                    elif(item[3] == 'L-Triple'):
                        pyautogui.click(clicks=3, button='left', x=item[4], y=item[5])
                    elif(item[3] == 'Move'):
                        pyautogui.moveTo(item[4], item[5])
                    elif(item[3] == 'Drag'):
                        pyautogui.dragTo(item[4], item[5], 0.5, button='left')
                    else:
                        print('somethings wrong (mouse)')
                    
                elif(item[2] == 'Keyboard'):
                    if(item[6] == 'Press'):
                        pyautogui.press(item[7])
                    elif(item[6] == 'KeyDown'):
                        pyautogui.keyDown(item[7])
                    elif(item[6] == 'KeyUp'):
                        pyautogui.keyUp(item[7])
                    else:
                        print('somethings wrong (keyboard)')

                elif(item[2] == 'Hotkey'):
                    spl = item[8].split('+')
                    if(len(spl) == 2):
                        pyautogui.hotkey(spl[0], spl[1])
                    elif(len(spl) == 3):
                        pyautogui.hotkey(spl[0], spl[1], spl[2])
                    else:
                        print('somethings wrong (hotkey)')

                elif(item[2] == 'WriteText'):
                    # pyautogui.write(item[9])  #it doesn't work in 한글
                    keyboard.write(item[9])
                else:
                    print('somethings wrong 1')

                if(thd1_bool == False):
                    break
                else:
                    time.sleep(item[10])

            else:
                print('somethings wrong 2')

        if(thd1_bool == False): break

    thd1_bool = False
    allWidgetsActDeact()
    targetCrossActDeact(True)
    start_btn.config(bg='#F0F0F0')
    print('thread done!')
  
#targetpoint(+) show or hide
def targetShowHide():
    if(len(target_win_arr) == 0):
        pass
    else:
        if(show_hide_chk_var.get()):
            for idx, item in enumerate(target_win_arr):
                if(select_func_combo_arr[idx].get() == 'Mouse'):    #if select function is Mouse, 
                    item.deiconify()     #show target window
                else:
                    pass
        else:
            for item in target_win_arr:
                item.withdraw()
    

#disable comboboxes not necessary 
def actDeactWidgets(event):
    t_cnt = len(target_win_arr)
    for idx in range(0, t_cnt):
        if(select_func_combo_arr[idx].get() == 'Mouse'):
            act_chk_btn_arr         [idx].config(state='normal')
            select_func_combo_arr   [idx].config(state='readonly')
            mouse_func_combo_arr    [idx].config(state='readonly')
            key_func_combo_arr      [idx].config(state='disabled')
            key_combo_arr           [idx].config(state='disabled')
            hotkey_combo_arr        [idx].config(state='disabled')
            text_entry_arr          [idx].config(state='readonly')
            delay_entry_arr         [idx].config(stat='normal')
            target_win_arr          [idx].deiconify()     #show target window
        elif(select_func_combo_arr[idx].get() == 'Keyboard'):
            act_chk_btn_arr         [idx].config(state='normal')
            select_func_combo_arr   [idx].config(state='readonly')
            mouse_func_combo_arr    [idx].config(state='disabled')
            key_func_combo_arr      [idx].config(state='readonly')
            key_combo_arr           [idx].config(state='readonly')
            hotkey_combo_arr        [idx].config(state='disabled')
            text_entry_arr          [idx].config(state='readonly')
            delay_entry_arr         [idx].config(stat='normal')
            target_win_arr          [idx].withdraw()     #hide target window
        elif(select_func_combo_arr[idx].get() == 'Hotkey'):
            act_chk_btn_arr         [idx].config(state='normal')
            select_func_combo_arr   [idx].config(state='readonly')
            mouse_func_combo_arr    [idx].config(state='disabled')
            key_func_combo_arr      [idx].config(state='disabled')
            key_combo_arr           [idx].config(state='disabled')
            hotkey_combo_arr        [idx].config(state='readonly')
            text_entry_arr          [idx].config(state='readonly')
            delay_entry_arr         [idx].config(stat='normal')
            target_win_arr          [idx].withdraw()     #hide target window
        elif(select_func_combo_arr[idx].get() == 'WriteText'):
            act_chk_btn_arr         [idx].config(state='normal')
            select_func_combo_arr   [idx].config(state='readonly')
            mouse_func_combo_arr    [idx].config(state='disabled')
            key_func_combo_arr      [idx].config(state='disabled')
            key_combo_arr           [idx].config(state='disabled')
            hotkey_combo_arr        [idx].config(state='disabled')
            text_entry_arr          [idx].config(state='normal')
            delay_entry_arr         [idx].config(stat='normal')
            target_win_arr          [idx].withdraw()     #hide target window
        
       
#when thread is running, all of widgets are Deactivated
def allWidgetsActDeact():
    if(thd1_bool):
        init_delay_entry            .config(state='readonly')
        loop_entry                  .config(state='readonly')
        t_cnt = len(target_win_arr)
        for idx in range(0, t_cnt):
            act_chk_btn_arr         [idx].config(state='disabled')
            select_func_combo_arr   [idx].config(state='disabled')
            mouse_func_combo_arr    [idx].config(state='disabled')
            key_func_combo_arr      [idx].config(state='disabled')
            key_combo_arr           [idx].config(state='disabled')
            hotkey_combo_arr        [idx].config(state='disabled')
            text_entry_arr          [idx].config(state='readonly')
            delay_entry_arr         [idx].config(stat='readonly')
    else:
        init_delay_entry            .config(state='normal')
        loop_entry                  .config(state='normal')
        actDeactWidgets('')
    
#save to json file
def saveFile():
    try:
        filename = filedialog.asksaveasfilename(initialdir="/", title="Save File",
                                                filetypes=(("Json", "*.json")))
        saveCondition()
        if(len(save_condition_arr) == 0):
            messagebox.showwarning(title='Warning', message='Please add targets push the + button')
        else:
            file_data = OrderedDict()
            file_data['total_count']    = len(save_condition_arr)
            file_data['init_delay']     = init_delay_entry.get()
            file_data['loop']           = loop_entry.get()

            for idx, item in enumerate(save_condition_arr):
                file_data[str(idx)] ={
                    'num' : item[0],            
                    'act_deact_chk'     : item[1],
                    'select_func'       : item[2],
                    'mouse_func'        : item[3],
                    'mouseX'            : item[4],
                    'mouseY'            : item[5],
                    'key_func'          : item[6],
                    'key_combo'         : item[7],
                    'hotkey'            : item[8],
                    'text_ent'          : item[9],
                    'delay_ent'         : int(item[10]*1000),
                    'target_win_posX'   : item[11],
                    'target_win_posY'   : item[12]
                    }
            with open(filename+".json", 'w', encoding='utf-8') as make_file:
                json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
                messagebox.showinfo(title='Success', message='File saved successfully')
    except Exception as e:
        messagebox.showwarning(title='Warning', message=e)
        print('file save error :', e)  

#load json file 
def loadFile():
    try:
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("Json", "*.json"),
                                                ("all files", "*.*")))
        with open(filename, 'r', encoding='utf-8') as load_file:
            load_data = json.load(load_file)
        
        total_count = load_data["total_count"]
        init_delay  = load_data["init_delay"]
        loop        = load_data["loop"]
        init_delay_entry.delete(0, tk.END)
        init_delay_entry.insert(0, init_delay)
        loop_entry      .delete(0, tk.END)
        loop_entry      .insert(0, loop)

        t_cnt = len(target_win_arr)
        for idx in range(0, t_cnt):  delTarget()
            
        for idx in range(0, total_count):
            #set act_deact chk
            if(load_data[str(idx)]["act_deact_chk"]):
                act_deact=1
            else:
                act_deact=0

            #set select_func
            for idx_sel, item in enumerate(select_func_list):
                if(item == load_data[str(idx)]["select_func"]):
                    select_func = idx_sel
            
            #set mouse_func
            for idx_sel, item in enumerate(mouse_func_list):
                if(item == load_data[str(idx)]["mouse_func"]):
                    mouse_func = idx_sel
            
            #set key_func
            for idx_sel, item in enumerate(key_func_list):
                if(item == load_data[str(idx)]["key_func"]):
                    key_func = idx_sel

            # set key_combo
            key_combo=0
            for idx_sel, item in enumerate(key_list):
                if(item == load_data[str(idx)]["key_combo"]):
                    key_combo = idx_sel

            #set hotkey
            for idx_sel, item in enumerate(hotkey_list):
                if(item == load_data[str(idx)]["hotkey"]):
                    hotkey = idx_sel

            text_ent    = load_data[str(idx)]["text_ent"]
            delay_ent   = load_data[str(idx)]["delay_ent"]
            target_win_posX = load_data[str(idx)]["target_win_posX"]
            target_win_posY = load_data[str(idx)]["target_win_posY"]

            makeTarget(act_deact, select_func, mouse_func, key_func, key_combo, hotkey, text_ent, delay_ent, target_win_posX, target_win_posY)
        messagebox.showinfo(title='Success', message='File load successfully')

    except Exception as e:
        messagebox.showwarning(title='Warning', message=e)
        print('file save error :', e)


#################################  UI using tkinter
####set main_frame
main_frame = tk.Frame(window)
main_frame.pack(fill='both', expand=1)

####set canvas for y_scroll
canvas = tk.Canvas(main_frame)
canvas.pack(side='left', fill='both', expand=1)

####set scrollbar
scrollbar=ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

#mouse wheel func
def on_MouseWheel(event):
    # block wheel func when scroll is not available
    if canvas.yview() == (0.0, 1.0):
        return
    canvas.yview_scroll(int(-1*event.delta/120), "units")

####set mouse wheel
canvas.configure(yscrollcommand=scrollbar.set)
window.bind('<MouseWheel>', on_MouseWheel)

####set second_frame on the canvas
second_frame = tk.Frame(canvas)
canvas.create_window((0,0), window=second_frame, anchor='nw')

####set_init
set_init_lbframe    = tk.LabelFrame(second_frame, text='Set Initial values')
init_delay_lb       = tk.Label(set_init_lbframe, justify='right', text='Init delay(ms):')
init_delay_entry    = tk.Entry(set_init_lbframe, justify='right', width=8)
loop_lb             = tk.Label(set_init_lbframe, justify='right', text='Loop:', anchor='e')
loop_entry          = tk.Entry(set_init_lbframe, justify='right', width=8)
####set_init GRID
set_init_lbframe    .grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky='news')
init_delay_lb       .grid(row=0, column=0, padx=(5,0), pady=(5,0))
init_delay_entry    .grid(row=0, column=1, padx=(5,5), pady=(5,0))
init_delay_entry    .insert(0,'1000')
loop_lb             .grid(row=1, column=0, padx=(5,0), pady=(5,5), sticky='ew')
loop_entry          .grid(row=1, column=1, padx=(5,5), pady=(5,5))
loop_entry          .insert(0,'1')


####add_target_lbframe
add_target_lbframe  = tk.LabelFrame(second_frame, text='Add/Del Targets')
add_target_btn      = tk.Button(add_target_lbframe, text='+', width=3, height=1, font=font_15_bold, command=makeTarget) #command=lambda: command_args(arg1, arg2, arg3)
del_target_btn      = tk.Button(add_target_lbframe, text='-', width=3, height=1, font=font_15_bold, command=delTarget) #command=lambda: command_args(arg1, arg2, arg3)
####add_target_lbframe GRID
add_target_lbframe  .grid(row=0, column=1, sticky='news', padx=(5,0), pady=(5,0))
add_target_btn      .grid(row=0, column=0, sticky='news', padx=(5,0), pady=(5,0))
del_target_btn      .grid(row=0, column=1, sticky='news', padx=(5,5), pady=(5,0))


####Start_lbframe
start_lbframe       = tk.LabelFrame(second_frame, text='Start')
start_btn           = tk.Button(start_lbframe, text='▶', width=3, height=1, font=font_15_bold, command=threadStart)
####Start_lbframe GRID
start_lbframe       .grid(row=0, column=2, sticky='news', padx=(5,0), pady=(5,0))
start_btn           .grid(row=0, column=0, sticky='news', padx=(5,5), pady=(5,0))


####Stop_lbframe
stop_lbframe        = tk.LabelFrame(second_frame, text='Stop')
stop_lb1            = tk.Label(stop_lbframe, text='Push ''▶'' button OR', anchor='w')
stop_lb2            = tk.Label(stop_lbframe, text='Ctrl+Shift+Space', anchor='w')
####Stop_lbframe GRID
stop_lbframe        .grid(row=0, column=3, sticky='news', padx=(5,0), pady=(5,0))
stop_lb1            .grid(row=0, column=0, sticky='news', padx=(5,0), pady=(5,0))
stop_lb2            .grid(row=1, column=0, sticky='news', padx=(5,0), pady=(0,0))


####progress_lbframe
progress_lbframe    =tk.LabelFrame(second_frame, text='Progress')
prog_loop_lb1       =tk.Label(progress_lbframe, text='Loop :', anchor='e')
prog_loop_lb2       =tk.Label(progress_lbframe, text='000/000')
prog_element_lb1    =tk.Label(progress_lbframe, text='Element :', anchor='e')
prog_element_lb2    =tk.Label(progress_lbframe, text='000/000')
####progress_lbframe GRID
progress_lbframe    .grid(row=0, column=4, sticky='news', padx=(5,0), pady=(5,0))
prog_loop_lb1       .grid(row=0, column=0, sticky='news', padx=(5,0), pady=(5,0))
prog_loop_lb2       .grid(row=0, column=1, sticky='news', padx=(5,0), pady=(5,0))
prog_element_lb1    .grid(row=1, column=0, sticky='news', padx=(5,0), pady=(5,0))
prog_element_lb2    .grid(row=1, column=1, sticky='news', padx=(5,0), pady=(5,0))


####save_load_lbframe
save_load_lbframe   =tk.LabelFrame(second_frame, text='Save/Load')
save_btn            =tk.Button(save_load_lbframe, text='Save', width=6, height=2, command=saveFile)
load_btn            =tk.Button(save_load_lbframe, text='Load', width=6, height=2, command=loadFile)
####save_load_lbframe GRID
save_load_lbframe   .grid(row=0, column=5, sticky='news', padx=(5,0), pady=(5,0))
save_btn            .grid(row=0, column=0, sticky='news', padx=(5,0), pady=(5,0))
load_btn            .grid(row=0, column=1, sticky='news', padx=(5,5), pady=(5,0))


####show_hide_lbframe
show_hide_lbframe   =tk.LabelFrame(second_frame, text='Show/Hide')
show_hide_chk_var   =tk.IntVar()
show_hide_chk_btn   =ttk.Checkbutton(show_hide_lbframe, text='Show/Hide', variable=show_hide_chk_var, command=targetShowHide)
####show_hide_lbframe GRID
show_hide_lbframe   .grid(row=0, column=6, sticky='news', padx=(5,0), pady=(5,0))
show_hide_chk_btn   .grid(row=0, column=0, sticky='news', padx=(5,0), pady=(5,0))
show_hide_chk_var   .set(1)


####set_target_lbframe
set_target_lbframe  = tk.LabelFrame(second_frame, text='Set Targets')
#Act(chk_btn), No. , Select Func.(Mouse, Keyboard, Hotkey, Write Text), Mouse Func.(L-click, L-Down, L-Up, R-click, R-Down, R-Up, Double, Move, Drag), key Func.(Press, KeyDown, KeyUp), Key('a', 'b',...), Hotkey(Ctrl+A, Ctrl+C, Ctrl+V), Text, Delay
#it will execute just what you Act checked
#when you select Mouse, then M-Function menu will be activated
no_lb               = tk.Label(set_target_lbframe, anchor='center', text='No.')
act_lb              = tk.Label(set_target_lbframe, anchor='center', text='Act')
select_func_lb      = tk.Label(set_target_lbframe, anchor='center', width=12, text='Select Func.')
mouse_func_lb       = tk.Label(set_target_lbframe, anchor='center', width=12, text='Mouse Func.')
key_func_lb         = tk.Label(set_target_lbframe, anchor='center', width=12, text='Key Func')
key_lb              = tk.Label(set_target_lbframe, anchor='center', width=12, text='Key')
hotkey_lb           = tk.Label(set_target_lbframe, anchor='center', width=12, text='Hotkey')
text_lb             = tk.Label(set_target_lbframe, anchor='center', width=20, text='Text')
delay_lb            = tk.Label(set_target_lbframe, anchor='center', width=8, text='Delay(ms)')
#seperators
sep_v1              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v2              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v3              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v4              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v5              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v6              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v7              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v8              = ttk.Separator(set_target_lbframe, orient="vertical")
sep_h1              = ttk.Separator(set_target_lbframe, orient="horizontal")
####set_target_lbframe GRID
set_target_lbframe  .grid(row=1, column=0, padx=(5,0), pady=(5,0), sticky='news', rowspan=999, columnspan=20)
no_lb               .grid(row=0, column=0, padx=(5,5), pady=(5,0))
sep_v1              .grid(row=0, column=1, sticky='ns', rowspan=999)
act_lb              .grid(row=0, column=2, padx=(5,5), pady=(5,0))
sep_v2              .grid(row=0, column=3, sticky='ns', rowspan=999)
select_func_lb      .grid(row=0, column=4, padx=(5,5), pady=(5,0))
sep_v3              .grid(row=0, column=5, sticky='ns', rowspan=999)
mouse_func_lb       .grid(row=0, column=6, padx=(5,5), pady=(5,0))
sep_v4              .grid(row=0, column=7, sticky='ns', rowspan=999)
key_func_lb         .grid(row=0, column=8, padx=(5,5), pady=(5,0))
sep_v5              .grid(row=0, column=9, sticky='ns', rowspan=999)
key_lb              .grid(row=0, column=10, padx=(5,5), pady=(5,0))
sep_v6              .grid(row=0, column=11, sticky='ns', rowspan=999)
hotkey_lb           .grid(row=0, column=12, padx=(5,5), pady=(5,0))
sep_v7              .grid(row=0, column=13, sticky='ns', rowspan=999)
text_lb             .grid(row=0, column=14, padx=(5,5), pady=(5,0))
sep_v8              .grid(row=0, column=15, sticky='ns', rowspan=999)
delay_lb            .grid(row=0, column=16, padx=(5,5), pady=(5,0))
sep_h1              .grid(row=1, column=0, sticky='ew', columnspan=17) 



#only digit input
def onlyNumbers(event):
    txt = event.widget.get()
    txt = re.sub(r"[^0-9]", "", txt)
    event.widget.delete(0,'end')
    event.widget.insert(0, txt)

#only digit input
init_delay_entry.bind('<KeyRelease>', onlyNumbers)
loop_entry      .bind('<KeyRelease>', onlyNumbers)

#thread stop hotkey
keyboard.add_hotkey('ctrl+shift+space', threadStop)


# 종료시 호출
def on_closing():
    global thd1_bool
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        thd1_bool = False
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
