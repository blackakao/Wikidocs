import os
import pyautogui as pag 
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import win32com.client as win32
from time import sleep
import pyperclip as cb


# root = Tk()
# filename = askopenfilename()
# root.destroy()
# BASE_DIR = os.path.dirname(filename)
# filename = os.path.basename(filename)

hwp = win32.Dispatch("HWPFrame.HwpObject")
# hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
hwp.Open("E:\\WindowApps\\청구서.hwp")
hwp.XHwpWindows.Item(0).Visible = True
# hwp.XHwpWindows.Item(0).Visible = True
# hwp.HAction.Run("FrameFullScreen")

# hwp.GetFielList()


# hwp.Open("C:\\Users\\실버킹\\Desktop\\[양식]근로계약서_김경율")
# hwp.XHwpWindows.Item(0).Visible = True
