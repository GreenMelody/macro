from sqlite3 import Row
import pyautogui
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
# pyautogui.moveTo(10,10, duration=2)


window = tk.Tk()
window.title('Tnank you for your help')
window.geometry('1500x400+0+0')
window.resizable(True,True)

font_15 = font.Font(size=15)
font_15_bold = font.Font(size=15, weight='bold')

select_func_list = ['Mouse', 'Keyboard', 'Hotkey', 'Write' 'Text']
mouse_func_list = ['L-Click', 'L-Down', 'L-Up', 'R-Click', 'R-Down', 'R-Up', 'Double', 'Move', 'Drag']
key_func_list = ['Press', 'KeyDown', 'KeyUp']
key_list = ['a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7','8', '9',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
            'space', 'backspace', 'tab', 'alt', 'altleft', 'altright', 'ctrl', 'ctrlleft', 'ctrlright', 'shift', 'shiftleft', 'shiftright', 'del', 'delete', 'left', 'right', 'up', 'down', 'end', 'enter', 'esc', 'escape', 'hanguel', 'hangul', 'home', 'insert',
            'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'printscreen', 'prntscrn', 'scrolllock',
            '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',  ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
            

hotkey_list = ['Ctrl+A', 'Ctrl+C', 'Ctrl+V']


save_condition_arr=[]             #save all things, [act/deact, num, select_func, mouse_func, mouse_X, mouseY, key_func, key, hotkey, text, delay]

t_cnt=0                 #total target window number
target_win_arr=[]       #save target windows
target_lb1_arr=[]       #target number label
target_lb2_arr=[]       #'+' label 
act_chk_btn_arr=[]      #act/deactive check box 
chk_var=[]
no_lb_arr=[]
select_func_combo_arr=[]
mouse_func_combo_arr=[]
key_func_combo_arr=[]
key_combo_arr=[]
hotkey_combo_arr=[]
text_entry_arr=[]
delay_entry_arr=[]

#make new target window
def makeTarget():
    #make new window and setting
    t_cnt = len(target_win_arr)
    target_win_arr.append(tk.Toplevel(window))
    target_win_arr[t_cnt].wm_attributes("-topmost", True)
    target_win_arr[t_cnt].wm_attributes("-transparentcolor", '#F0F0F0')      #to make window transparent
    target_win_arr[t_cnt].geometry('150x100')
    target_win_arr[t_cnt].overrideredirect(True)

    #show target num and target point '+'
    target_lb1_arr.append(tk.Label(target_win_arr[t_cnt], borderwidth=1, relief='ridge', bg='red', text='1111'))
    target_lb2_arr.append(tk.Label(target_win_arr[t_cnt], borderwidth=1, relief='ridge', width=3, font=font_15, fg='red', text='+'))
    target_lb1_arr[t_cnt].grid(row=0, column=0,sticky='ns')
    target_lb2_arr[t_cnt].grid(row=0, column=1)    

    #create checkbutton, label, combobox, entry
    chk_var.append(tk.IntVar())
    act_chk_btn_arr         .append(ttk.Checkbutton(set_target_lbframe, variable=chk_var[t_cnt]))
    no_lb_arr               .append(tk.Label(set_target_lbframe, text=str(t_cnt+1)))
    select_func_combo_arr .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=select_func_list))
    mouse_func_combo_arr  .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=mouse_func_list))
    key_func_combo_arr    .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=key_func_list))
    key_combo_arr         .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=key_list))
    hotkey_combo_arr      .append(ttk.Combobox(set_target_lbframe, state='readonly', width=8, values=hotkey_list))
    text_entry_arr          .append(tk.Entry(set_target_lbframe))
    delay_entry_arr         .append(tk.Entry(set_target_lbframe, justify='right', width=8))

    #grid checkbutton, label, combobox, entry
    act_chk_btn_arr[t_cnt]          .grid(row=t_cnt+2, column=0, padx=(5,5), pady=(5,0))
    no_lb_arr[t_cnt]                .grid(row=t_cnt+2, column=2, padx=(5,5), pady=(5,0))
    select_func_combo_arr[t_cnt]    .grid(row=t_cnt+2, column=4, padx=(5,5), pady=(5,0))
    mouse_func_combo_arr[t_cnt]     .grid(row=t_cnt+2, column=6, padx=(5,5), pady=(5,0))
    key_func_combo_arr[t_cnt]       .grid(row=t_cnt+2, column=8, padx=(5,5), pady=(5,0))
    key_combo_arr[t_cnt]            .grid(row=t_cnt+2, column=10, padx=(5,5), pady=(5,0))
    hotkey_combo_arr[t_cnt]         .grid(row=t_cnt+2, column=12, padx=(5,5), pady=(5,0))
    text_entry_arr[t_cnt]           .grid(row=t_cnt+2, column=14, padx=(5,5), pady=(5,0))
    delay_entry_arr[t_cnt]          .grid(row=t_cnt+2, column=16, padx=(5,5), pady=(5,0))

    chk_var[t_cnt].set(1)                       #always checked when it created
    select_func_combo_arr[t_cnt].current(0)     #select first value
    mouse_func_combo_arr[t_cnt].current(0)     #select first value
    key_func_combo_arr[t_cnt].current(0)     #select first value
    key_combo_arr[t_cnt].current(0)     #select first value
    hotkey_combo_arr[t_cnt].current(0)     #select first value
    actDeactWidgets('')
    #to move target point using mouse drag
    def drag(event):
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


#delete target and list
def delTarget():
    t_cnt = len(target_win_arr)
    if t_cnt != 0:
        #destroy widgets
        target_lb1_arr[t_cnt-1].destroy()
        target_lb2_arr[t_cnt-1].destroy()
        target_win_arr[t_cnt-1].destroy()
        act_chk_btn_arr[t_cnt-1].destroy()
        no_lb_arr[t_cnt-1].destroy() 
        select_func_combo_arr[t_cnt-1].destroy()
        mouse_func_combo_arr[t_cnt-1].destroy()
        key_func_combo_arr[t_cnt-1].destroy()
        key_combo_arr[t_cnt-1].destroy()
        hotkey_combo_arr[t_cnt-1].destroy()
        text_entry_arr[t_cnt-1].destroy()
        delay_entry_arr[t_cnt-1].destroy()

        #remove list
        target_lb1_arr.pop()
        target_lb2_arr.pop()
        target_win_arr.pop()
        act_chk_btn_arr.pop()
        no_lb_arr.pop() 
        select_func_combo_arr.pop()
        mouse_func_combo_arr.pop()
        key_func_combo_arr.pop()
        key_combo_arr.pop()
        hotkey_combo_arr.pop()
        text_entry_arr.pop()
        delay_entry_arr.pop()
        chk_var.pop()
    else:
        print('no widget to delete')

#when you push the start button, it will save target points and ect. only act checked
def saveCondition():
    save_condition_arr=[]
    t_cnt = len(target_win_arr)
    for idx in range(0, t_cnt):
        act_deact = chk_var[idx].get()
        num = no_lb_arr[idx].cget('text')
        select_func = select_func_combo_arr[idx].get()
        mouse_func = mouse_func_combo_arr[idx].get()
        #mouse target point X,Y
        mouseX=target_lb2_arr[idx].winfo_rootx() + (target_lb2_arr[idx].winfo_width())/2
        print('mx :',mouseX)
        mouseY=target_lb2_arr[idx].winfo_rooty() + (target_lb2_arr[idx].winfo_height())/2
        print('my :',mouseY)
        key_func = key_func_combo_arr[idx].get()
        hotkey = hotkey_combo_arr[idx].get()
        text_ent = text_entry_arr[idx].get()
        delay_ent = delay_entry_arr[idx].get()
        save_condition_arr.append([act_deact,num,select_func,mouse_func,key_func,hotkey,text_ent,delay_ent])

def play():
    pyautogui.moveTo(-63.5, 138,2)
    pass
  
#disable comboboxes not necessary 
def actDeactWidgets(event):
    t_cnt = len(target_win_arr)
    for idx in range(0, t_cnt):
        if(select_func_combo_arr[idx].get() == 'Mouse'):
            mouse_func_combo_arr[idx].config(state='readonly')
            key_func_combo_arr[idx].config(state='disabled')
            key_combo_arr[idx].config(state='disabled')
            hotkey_combo_arr[idx].config(state='disabled')
            text_entry_arr[idx].config(state='readonly')
        elif(select_func_combo_arr[idx].get() == 'Keyboard'):
            mouse_func_combo_arr[idx].config(state='disabled')
            key_func_combo_arr[idx].config(state='readonly')
            key_combo_arr[idx].config(state='readonly')
            hotkey_combo_arr[idx].config(state='disabled')
            text_entry_arr[idx].config(state='readonly')
        elif(select_func_combo_arr[idx].get() == 'Hotkey'):
            mouse_func_combo_arr[idx].config(state='disabled')
            key_func_combo_arr[idx].config(state='disabled')
            key_combo_arr[idx].config(state='disabled')
            hotkey_combo_arr[idx].config(state='readonly')
            text_entry_arr[idx].config(state='readonly')
        elif(select_func_combo_arr[idx].get() == 'WriteText'):
            mouse_func_combo_arr[idx].config(state='disabled')
            key_func_combo_arr[idx].config(state='disabled')
            key_combo_arr[idx].config(state='disabled')
            hotkey_combo_arr[idx].config(state='disabled')
            text_entry_arr[idx].config(state='normal')
        
       

def allWidgetsActDeact():
    pass











#################################  UI using tkinter

####set_init
set_init_lbframe = tk.LabelFrame(window, text='Set Initial values')
init_delay_lb = tk.Label(set_init_lbframe, text='Init delay(ms) : ')
init_delay_entry = tk.Entry(set_init_lbframe, justify='right', width=8)

####set_init GRID
set_init_lbframe    .grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky='news')
init_delay_lb       .grid(row=0, column=0, padx=(5,0), pady=(5,0))
init_delay_entry    .grid(row=0, column=1, padx=(5,0), pady=(5,0))


####set_target_lbframe
set_target_lbframe = tk.LabelFrame(window, text='Set Targets')
#Act(chk_btn), No. , Select Func.(Mouse, Keyboard, Hotkey, Write Text), Mouse Func.(L-click, L-Down, L-Up, R-click, R-Down, R-Up, Double, Move, Drag), key Func.(Press, KeyDown, KeyUp), Key('a', 'b',...), Hotkey(Ctrl+A, Ctrl+C, Ctrl+V), Text, Delay
#it will execute just what you Act checked
#when you select Mouse, then M-Function menu will be activated
act_lb          = tk.Label(set_target_lbframe, anchor='center', text='Act')
no_lb           = tk.Label(set_target_lbframe, anchor='center', text='No.')
select_func_lb  = tk.Label(set_target_lbframe, anchor='center', width=12, text='Select Func.')
mouse_func_lb   = tk.Label(set_target_lbframe, anchor='center', width=12, text='Mouse Func.')
key_func_lb     = tk.Label(set_target_lbframe, anchor='center', width=12, text='Key Func')
key_lb          = tk.Label(set_target_lbframe, anchor='center', width=12, text='Key')
hotkey_lb       = tk.Label(set_target_lbframe, anchor='center', width=12, text='Hotkey')
text_lb         = tk.Label(set_target_lbframe, anchor='center', width=20, text='Text')
delay_lb        = tk.Label(set_target_lbframe, anchor='center', width=8, text='Delay(ms)')
#seperators
sep_v1          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v2          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v3          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v4          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v5          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v6          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v7          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_v8          = ttk.Separator(set_target_lbframe, orient="vertical")
sep_h1          = ttk.Separator(set_target_lbframe, orient="horizontal")

####set_target_lbframe GRID
set_target_lbframe  .grid(row=1, column=0, padx=(5,0), pady=(5,0), sticky='news', rowspan=999)
act_lb              .grid(row=0, column=0, padx=(5,5), pady=(5,0))
sep_v1              .grid(row=0, column=1, sticky='ns', rowspan=999)
no_lb               .grid(row=0, column=2, padx=(5,5), pady=(5,0))
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
delay_lb             .grid(row=0, column=16, padx=(5,5), pady=(5,0))
sep_h1              .grid(row=1, column=0, sticky='ew', columnspan=17) 



####add_target_lbframe
add_target_lbframe = tk.LabelFrame(window, text='Add/Del Targets')
add_target_btn = tk.Button(add_target_lbframe, text='+', width=2, height=1, font=font_15_bold, command=makeTarget) #command=lambda: command_args(arg1, arg2, arg3)
del_target_btn = tk.Button(add_target_lbframe, text='-', width=2, height=1, font=font_15_bold, command=delTarget) #command=lambda: command_args(arg1, arg2, arg3)

####add_target_lbframe GRID
add_target_lbframe  .grid(row=0, column=1, sticky='news', padx=(5,0), pady=(5,0))
add_target_btn      .grid(row=0, column=2)
del_target_btn      .grid(row=0, column=9)


test2_btn = tk.Button(add_target_lbframe, text='get target point', command=saveCondition)
test3_btn = tk.Button(add_target_lbframe, text='move to target point', command=play)




        




test2_btn.grid(row=2, column=0)
test3_btn.grid(row=3, column=0)






#only digit input
def onlyNumbers(event):
    if str.isdigit(event.char):
        
        print(event.char)
    else:
        txt = str(init_delay_entry.get())
        #init_delay_entry.delete(0,'end')
        #init_delay_entry.insert(0, txt[:-1])
        init_delay_entry.delete(0,'end')
        init_delay_entry.insert(0, txt[:-1])




#only digit input
init_delay_entry.bind('<KeyRelease>', onlyNumbers)



window.mainloop()