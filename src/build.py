import PyInstaller.__main__


install_folder = "install/"
build_folder = "install/build"
dist_folder = "install/dist"
program_name = "Autosa"
python_file_path = "src/main.py"
# iconPath = "tenco-favicon-192x192.ico"

PyInstaller.__main__.run(
    [
        python_file_path,
        "--workpath",
        build_folder,
        "--distpath",
        dist_folder,
        "--specpath",
        install_folder,
        "--name",
        program_name,
        # "--icon",
        # iconPath,
        "--onefile",
        "--windowed",
        "--clean",
    ]
)
