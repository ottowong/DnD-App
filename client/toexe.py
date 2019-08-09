from cx_Freeze import setup, Executable 

setup(name = "DnD App" , 
      version = "1.0" , 
      description = "" , 
      executables = [Executable("main.py", base="Win32GUI", icon="icon.ico")]) 
# base="Win32GUI",