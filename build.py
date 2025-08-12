
import os
import subprocess
import shutil

HERE = os.path.abspath(os.path.dirname(__file__))

def build_external():
#-- The actual cmake-based build steps for JIGSAW

    cwd_pointer = os.getcwd()

    try:
        print("cmake config. for jigsaw...")

        source_path = os.path.join(
            HERE, "external", "jigsaw")

        builds_path = \
            os.path.join(source_path, "tmp")

        os.makedirs(builds_path, exist_ok=True)

        exesrc_path = \
            os.path.join(source_path, "bin")

        libsrc_path = \
            os.path.join(source_path, "lib")

        exedst_path = os.path.join(
            HERE, "jigsawpy", "_bin")

        libdst_path = os.path.join(
            HERE, "jigsawpy", "_lib")

        shutil.rmtree(
            exedst_path, ignore_errors=True)
        shutil.rmtree(
            libdst_path, ignore_errors=True)

        os.chdir(builds_path)

        config_call = [
            "cmake",
            "..", "-DCMAKE_BUILD_TYPE=Release"]

        subprocess.run(config_call, check=True)

        print("cmake compile for jigsaw...")

        try:            
            compilecall = [
                "cmake", "--build", ".",
                "--config", "Release",
                "--target", "install",
                "--parallel", "4"
                ]
            subprocess.run(
                compilecall, check=True)

        except:
            compilecall = [
                "cmake", "--build", ".",
                "--config", "Release",
                "--target", "install"
                ]
            subprocess.run(
                compilecall, check=True)

        print("cmake cleanup for jigsaw...")

        shutil.copytree(exesrc_path, exedst_path)
        shutil.copytree(libsrc_path, libdst_path)

    finally:
        os.chdir(cwd_pointer)

        shutil.rmtree(builds_path)


if (__name__ == "__main__"): build_external()

