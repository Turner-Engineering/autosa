import PyInstaller.__main__


installFolder = "install/"
buildFolder = "install/build"
distFolder = "install/dist"
programName = "Autosa"
mainPythonFile = "src/main.py"

PyInstaller.__main__.run(
    [
        mainPythonFile,
        "--onefile",
        "--windowed",
        "--workpath",
        buildFolder,
        "--distpath",
        distFolder,
        "--specpath",
        installFolder,
        "--name",
        programName,
    ]
)
