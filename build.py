
import os
import subprocess
import shutil
import argparse

HERE = os.path.abspath(os.path.dirname(__file__))

def build_external(build_type="Release", 
                   netcdf_user_path=None,
                   openmp_user_path=None
                   ):
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
            "cmake", "..", 
        "-DCMAKE_BUILD_TYPE=" + build_type]

        if (netcdf_user_path is not None):
            config_call+= [
        "-DNETCDF_USER_PATH="+netcdf_user_path]

        if (openmp_user_path is not None):
            config_call+= [
        "-DOPENMP_USER_PATH="+openmp_user_path]

        print(config_call)
        subprocess.run(config_call, check=True)

        print("cmake compile for jigsaw...")

        try:            
            compilecall = [
                "cmake", "--build", ".",
                "--config", build_type,
                "--target", "install",
                "--parallel", "4"
                ]
            subprocess.run(
                compilecall, check=True)

        except:
            compilecall = [
                "cmake", "--build", ".",
                "--config", build_type,
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


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--cmake-build-type", dest="cmake_build_type",
        required=False,
        type=str, default="Release", 
        help="Build JIGSAW in {Release}, Debug mode.")

    parser.add_argument(
        "--netcdf-user-path", dest="netcdf_user_path",
        required=False,
        type=str, default=None,
        help="(Optional) dir. containing netcdf lib.")

    parser.add_argument(
        "--openmp-user-path", dest="openmp_user_path",
        required=False,
        type=str, default=None,
        help="(Optional) dir. containing openmp lib.")

    args = parser.parse_args()

    build_external(args.cmake_build_type,
                   args.netcdf_user_path,
                   args.openmp_user_path)

