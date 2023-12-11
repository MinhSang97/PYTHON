# file: setup.py
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("main.py", base=base)
]

build_exe_options = {
    "include_files": ["path/to/your/icon.ico"],
    "packages": [
        "tkinter", "pyodbc", "pandas", "configparser", "openpyxl", "PIL", "ctypes"
    ],
    "include_msvcr": True,
    "excludes": []
}

setup(
    name="HHM_MSSQL",
    version="1.0",
    description="Description of your application",
    options={
        "build_exe": build_exe_options
    },
    executables=executables
)
