from tkinter import *
from tkinter import messagebox

list_branch = ["분당점", "탄현점", "일산본점", "수원점", "김포점", "양평실버타운", "분당3관"]

def clickButton(branch_number):
    messagebox.showinfo("케어포 이동", "%d 케어포 이동" %branch_number)
    
window = Tk()
window.title("케어포 로그인 어플")
window.geometry("300x300")
window.resizable(width=FALSE, height=FALSE)

# 버튼 만드는 구간 나중에는 리스트해서 자동으로 추가할 수 있도록 바꾸자...

btnList = [None] * 7

for i in range(0,7):
    btnList[i] = Button(window, text=list_branch[i], command=clickButton(i))
    
# for btn in btnList:
#     btn.pack(side=RIGHT)

btnList[0].pack()
btnList[1].pack()
btnList[2].pack()
btnList[3].pack()
btnList[4].pack()
btnList[5].pack()
btnList[6].pack()

window.mainloop()
    