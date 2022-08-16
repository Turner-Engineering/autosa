import PyInstaller.__main__


PyInstaller.__main__.run(
    [
        "src/main.py",
        "--onefile",
        "--windowed",
        "--workpath",
        "install/build",
        "--distpath",
        "install/dist",
        "--specpath",
        "install/",
        "--name",
        "Autosa",
    ]
)
