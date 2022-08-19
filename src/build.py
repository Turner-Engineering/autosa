import PyInstaller.__main__


installFolder = "install/"
buildFolder = "install/build"
distFolder = "install/dist"
programName = "Autosa"
pythonFilePath = "src/main.py"
# iconPath = "tenco-favicon-192x192.ico"

PyInstaller.__main__.run(
    [
        pythonFilePath,
        "--workpath",
        buildFolder,
        "--distpath",
        distFolder,
        "--specpath",
        installFolder,
        "--name",
        programName,
        # "--icon",
        # iconPath,
        "--onefile",
        "--windowed",
        "--clean"
    ]
)
