project(cmake_wrapper)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
# The TARGET parameter prevents the setup of global link/include directives
# We don't want to include/link everything!
conan_basic_setup(TARGETS)

find_package(OpenAL)
# The provided FindOpenAL.cmake don't declares this correctly:
set(OPENAL_INCLUDE_DIR ${CONAN_INCLUDE_DIRS})

# These have proper CMake support in their Conan packages:
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
        set(FLAC_LIBRARY_DIRS ${CONAN_LIB_DIRS_FLAC})
    endif()

    # ALUREs dynload feature needs this:
    set(LIBFLAC_LIBRARIES "${FLAC_LIBRARY}")

    set(FLAC_FOUND TRUE)
endif()

# The MPG123 library has no CMake support in its Conan package:
if(NOT MPG123_FOUND)
    if(NOT MPG123_INCLUDE_DIR)
        find_path(MPG123_INCLUDE_DIR
                  NAMES mpg123.h
                  PATHS ${CONAN_INCLUDE_DIRS_MPG123})
        set(MPG123_INCLUDE_DIRS ${MPG123_INCLUDE_DIR})
    endif()

    if(NOT MPG123_LIBRARY)
        find_library(MPG123_LIBRARY
                     ${CONAN_LIBS_MPG123}
                     PATHS ${CONAN_LIB_DIRS_MPG123})
        set(MPG123_LIBRARIES ${MPG123_LIBRARY})
        set(MPG123_LIBRARY_DIRS ${CONAN_LIB_DIRS_MPG123})
    endif()

    set(MPG123_FOUND TRUE)
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/source_subfolder/cmake")
add_subdirectory("source_subfolder")
