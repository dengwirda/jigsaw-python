function (cfg_compile_options OPT CFG)
  add_compile_options ("$<$<CONFIG:${CFG}>:${OPT}>")
endfunction ()

set (CMAKE_CXX_STANDARD 17)
set (CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)


if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU"   OR
    CMAKE_CXX_COMPILER_ID STREQUAL "Clang" OR
    CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
  set (GCXX_LIKE TRUE)
  message (">> GCXX-like compiler detected")
endif ()

if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set (MSVC_LIKE TRUE)
  message (">> MSVC-like compiler detected")
endif ()

if (DEFINED MSVC_LIKE)
  add_compile_options (/W3)
  cfg_compile_options (/GS- RELEASE)
  cfg_compile_options (/Ot  RELEASE)
endif ()

if (DEFINED GCXX_LIKE)
  add_compile_options (-pedantic -Wall -pthread -fopenmp)
endif ()

if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set (INSTALL_LOCAL TRUE)
  message (">> Installing locally")
else ()
  message (">> Installing to ${CMAKE_INSTALL_PREFIX}")
endif ()

find_library (NETCDF_LIBRARY NAMES netcdf)

if (NETCDF_LIBRARY)
  message (">> NetCDF library found")
  message (STATUS "NetCDF inc. lib: ${NETCDF_LIBRARY}")
else ()
  message (">> NetCDF library not found")
endif ()


add_executable (jigsaw-cmd jigsaw.cpp)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
target_link_libraries(jigsaw-cmd PRIVATE Threads::Threads)
#if (NETCDF_LIBRARY)
#  target_compile_definitions (jigsaw-cmd PRIVATE CMD_JIGSAW USE_NETCDF)
#  target_link_libraries (jigsaw-cmd ${NETCDF_LIBRARY})
#  set_target_properties (jigsaw-cmd PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE)
#else ()
#  target_compile_definitions (jigsaw-cmd PRIVATE CMD_JIGSAW)
#endif ()

set_target_properties (jigsaw-cmd PROPERTIES OUTPUT_NAME jigsaw)
if (DEFINED INSTALL_LOCAL)
  install (TARGETS jigsaw-cmd DESTINATION "${PROJECT_SOURCE_DIR}/bin")
else ()
  install (TARGETS jigsaw-cmd DESTINATION bin)
endif ()
