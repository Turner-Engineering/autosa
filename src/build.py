import json
import PyInstaller.__main__

with open("src/version.json", "r") as reader:
    autosa_version = json.load(reader)["__version__"]

install_folder = "install/"
build_folder = "install/build"
dist_folder = "install/dist"
program_name = f"Autosa_v{autosa_version}"
python_file_path = "src/main.py"
datas = "../src/images;./images"
version_data = "../src/version.json;."

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
    ]
)
