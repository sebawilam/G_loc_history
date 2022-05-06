# -*- coding: utf-8 -*-
"""
Created on Thu May  5 21:22:23 2022

@author: Seba
"""

def fl_dialog():
    import tkinter as tk
    from tkinter import filedialog
    
    root = tk.Tk()
    root.withdraw()
    global file_path
    file_path = filedialog.askopenfilename()
    return file_path