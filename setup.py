from cx_Freeze import setup, Executable

# Inclua os arquivos adicionais que seu aplicativo precisa
build_exe_options = {
    "packages": ["os", "requests"],
    "includes": ["PyQt5"],
    "include_files": []
}

setup(
    name="hola",
    version="1.0.0",
    description="Descrição do seu aplicativo",
    options={"build_exe": build_exe_options},
    executables=[Executable("hola_app.py", base="Win32GUI")]
)
