project(cmake_wrapper)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/source_subfolder/cmake")
add_subdirectory("source_subfolder")
