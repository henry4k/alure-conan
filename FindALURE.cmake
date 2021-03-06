find_path(ALURE_INCLUDE_DIR
          NAMES AL/alure.h
          PATHS ${CONAN_INCLUDE_DIRS_ALURE})
find_library(ALURE_LIBRARY
             NAMES ${CONAN_LIBS_ALURE}
             PATHS ${CONAN_LIB_DIRS_ALURE})
set(ALURE_FOUND TRUE)
set(ALURE_INCLUDE_DIRS ${ALURE_INCLUDE_DIR})
set(ALURE_LIBRARIES ${ALURE_LIBRARY})
mark_as_advanced(ALURE_LIBRARY ALURE_INCLUDE_DIR)
