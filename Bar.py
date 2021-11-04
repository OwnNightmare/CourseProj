# from tkinter import *
# from tkinter.ttk import *
# import time
# bar = Tk()
# bar.title('Uploading')
# bar.geometry('400x250+1000+300')
#
#
# def step():
#     for i in range(5):
#         bar.update_idletasks()
#         pb1['value'] += 20
#
#         time.sleep(1)
#
#
# pb1 = Progressbar(bar, orient=HORIZONTAL, length=100, mode='indeterminate')
# pb1.pack(expand=True)
#
# Button(bar, text='Start', command=step).pack()
#
# bar.mainloop()

from tqdm import tqdm
from time import sleep

for i in tqdm(range(100), desc='Blowjob', ):
    sleep(.01)


