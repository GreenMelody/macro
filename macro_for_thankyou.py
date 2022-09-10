from cgi import test
from distutils.spawn import spawn
from turtle import color
import pyautogui
import tkinter as tk
import tkinter.font as font
# pyautogui.moveTo(10,10, duration=2)


window = tk.Tk()
window.title('Tnank you for your help')
window.geometry('1000x400+0+0')
window.resizable(True,True)

target_point_arr=[]     #save target point absolute point
target_win_arr=[]       #save target windows

#make new target window
def makeTarget():
    targetUI = tk.Toplevel(window)
    targetUI.wm_attributes("-topmost", True)
    targetUI.wm_attributes("-transparentcolor", '#F0F0F0')      #to make window transparent
    targetUI.geometry('150x100')
    targetUI.overrideredirect(True)


    txt_font = font.Font(size=15)

    num_lb = tk.Label(targetUI, text='1111', borderwidth=1, relief='ridge', bg='red')
    target_point_lb = tk.Label(targetUI, text='+', borderwidth=1, relief='ridge', width=3, fg='red')
    target_point_lb['font'] = txt_font


    num_lb.grid(row=0, column=0,sticky='ns')
    target_point_lb.grid(row=0, column=1)    


    #to move target point using mouse drag
    def drag(event):
        width = str(targetUI.winfo_width())
        height = str(targetUI.winfo_height())
        pos_x = str(pyautogui.position().x)
        pos_y = str(pyautogui.position().y)
        targetUI.geometry(width + 'x' + height + '+' + pos_x + '+' + pos_y)

    #mouse left drag event
    num_lb.bind("<B1-Motion>", drag)



def getTargetPoint():
    pass

def moveToTargetPoint():
    pass


set_target_lbframe = tk.LabelFrame(window, text='Set Targets')
#Act(chk_btn), No. , Select-Func(Mouse, Keyboard, Write Text, Hotkey), M-Function(L-click, L-Down, L-Up, R-click, R-Down, R-Up, Double, Move, Drag), K-Function(Press, KeyDown, KeyUp), Keys HotKey(Ctrl+C, Ctrl)
#it will execute just what you Act checked
#when you select

test_btn = tk.Button(window, text='make new target', command=makeTarget) #command=lambda: command_args(arg1, arg2, arg3)
test2_btn = tk.Button(window, text='get target point', command=getTargetPoint)
test3_btn = tk.Button(window, text='move to target point', command=moveToTargetPoint)


set_target_lbframe.grid(row=0, column=0)
test_btn.grid(row=0, column=0)
test2_btn.grid(row=0, column=1)
test3_btn.grid(row=0, column=2)


window.mainloop()