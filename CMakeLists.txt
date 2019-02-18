project(cmake_wrapper)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
# The TARGET parameter prevents the setup of global link/include directives
# We don't want to include/link everything!
conan_basic_setup(TARGETS)

# These have proper CMake support in their Conan packages:
find_package(OpenAL)
find_package(OGG)
find_package(VORBIS)
# ALUREs dynload feature needs this:
set(VORBISFILE_LIBRARIES ${VORBISFILE_LIBRARY} ${VORBIS_LIBRARY} ${OGG_LIBRARY})

# The FLAC library has no CMake support in its Conan package:
if(NOT FLAC_FOUND)
    if(NOT FLAC_INCLUDE_DIR)
        find_path(FLAC_INCLUDE_DIR
                  NAMES FLAC/all.h
                  PATHS ${CONAN_INCLUDE_DIRS_FLAC})
        set(FLAC_INCLUDE_DIRS ${FLAC_INCLUDE_DIR})
    endif()

    if(NOT FLAC_LIBRARY)
        find_library(FLAC_LIBRARY
                     flac
                     PATHS ${CONAN_LIB_DIRS_FLAC})
        set(FLAC_LIBRARIES ${FLAC_LIBRARY})
    endif()

    # ALUREs dynload feature needs this:
    set(LIBFLAC_LIBRARIES "${FLAC_LIBRARY}")

    set(FLAC_FOUND TRUE)
    mark_as_advanced(FLAC_FOUND
                     FLAC_INCLUDE_DIR
                     FLAC_INCLUDE_DIRS
                     FLAC_LIBRARY
                     FLAC_LIBRARIES
                     LIBFLAC_LIBRARIES)

     message(STATUS ">>>>>>>>>>>>>>> ${FLAC_INCLUDE_DIR}")
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/source_subfolder/cmake")
add_subdirectory("source_subfolder")
