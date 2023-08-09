from pathlib import Path
import shutil
import subprocess
import platform

def build():
    src_parent = Path(__file__).parent.resolve()
    exedst_path = src_parent / "jigsawpy/_bin"
    libdst_path = src_parent / "jigsawpy/_lib"
    syslib = {"Windows": "jigsaw.dll", "Linux": "libjigsaw.so", "Darwin": "libjigsaw.dylib"}
    tgt_libsaw_path = libdst_path / syslib[platform.system()]
    if not tgt_libsaw_path.is_file():
        jigsaw_src_dir = src_parent / "external/jigsaw"
        cmake_build_dir = jigsaw_src_dir / "build"
        cmake_build_dir.mkdir(exist_ok=True)
        subprocess.run(
            [
                "cmake",
                '..',
                "-DCMAKE_BUILD_TYPE=Release",
                "-DCMAKE_INSTALL_PREFIX=."
            ],
            cwd=cmake_build_dir
            )
        subprocess.run(["make", f"-j4"], cwd=cmake_build_dir)
        subprocess.run(["make", f"-j4", "install"], cwd=cmake_build_dir)
        exesrc_path = cmake_build_dir / "bin"
        libsrc_path = cmake_build_dir / "lib"
        exedst_path = src_parent / "jigsawpy/_bin"
        libdst_path = src_parent / "jigsawpy/_lib"
        shutil.copytree(exesrc_path, exedst_path)
        shutil.copytree(libsrc_path, libdst_path)


build()