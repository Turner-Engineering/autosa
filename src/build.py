import PyInstaller.__main__

autosa_version = open("src/autosa_version.txt", "r").read()

install_folder = "install/"
build_folder = "install/build"
dist_folder = "install/dist"
program_name = f"Autosa_v{autosa_version}"
python_file_path = "src/main.py"
datas = "../src/images;./images"
version_data = "../src/autosa_version.txt;."
autosa_logo = "../src/images/autosa_logo.ico"

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
        "--add-data",
        datas,
        "--add-data",
        version_data,
        "--onefile",
        "--windowed",
        "--clean",
        "--icon=" + autosa_logo,
    ]
)
