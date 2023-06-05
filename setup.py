#crée une version .exe du projet en exécutant compile.bat

from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files":["data"],
    "optimize":2
}

# On appelle la fonction setup
setup(
    name = "slime",
    version = "1",
    description = "Votre programme",
    options={"build_exe": build_exe_options},
    executables = [Executable("main.py")],
)
