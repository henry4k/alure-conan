from conans import ConanFile, CMake, tools
import os


class AlureConan(ConanFile):
    name = "alure"
    version = "1.2"
    md5 = "77cbee1d57ec4ec7d9b3ffef19e08f76" # for the .tar.gz archive
    license = "MIT"
    author = "anon <anon@example.org>" # TODO
    url = "example.org" # TODO
    homepage = "https://kcat.strangesoft.net/alure.html"
    description = "ALURE is a utility library to help manage common tasks with OpenAL applications"
    topics = ("audio")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "dynload": [True, False]
    }
    default_options = "shared=False", "fPIC=True", "dynload=True"
    generators = "cmake"
    source_subfolder = "source_subfolder"
    exports_sources = ["CMakeLists.txt"]
    requires = (("ogg/1.3.3@bincrafters/stable"),
                ("vorbis/1.3.6@bincrafters/stable"),
                ("opus/1.2.1@bincrafters/stable"))

    def source(self):
        source_url_template = "https://kcat.strangesoft.net/alure-releases/alure-{0}.tar.gz"
        tools.get(source_url_template.format(self.version), self.md5)
        extracted_dir = "alure-{0}".format(self.version)
        os.rename(extracted_dir, self.source_subfolder)

        pattern = 'SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")\n'
        cmake_file = os.path.join(self.source_subfolder, 'CMakeLists.txt')
        tools.replace_in_file(cmake_file, pattern, '')

        tools.replace_in_file(os.path.join(self.source_subfolder,
                                           'cmake',
                                           'CheckFileOffsetBits.cmake'),
                              '${CMAKE_SOURCE_DIR}/cmake',
                              '${CMAKE_SOURCE_DIR}/'+self.source_subfolder+'/cmake')

    def build(self):
        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions['BUILD_SHARED'] = 'ON' if self.options.shared else 'OFF'
        cmake.definitions['BUILD_STATIC'] = 'ON' if not self.options.shared else 'OFF'
        cmake.definitions['DYNLOAD'] = 'ON' if self.options.dynload else 'OFF'
        cmake.definitions['SNDFILE'] = 'OFF'
        cmake.definitions['DUMB'] = 'OFF'
        cmake.definitions['MODPLUG'] = 'OFF'
        cmake.definitions['FLUIDSYNTH'] = 'OFF'
        cmake.definitions['BUILD_EXAMPLES'] = 'OFF'
        cmake.definitions['INSTALL_EXAMPLES'] = 'OFF'
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("COPYING", dst="licenses", keep_path=False)

    #def package_info(self):
    #    if self.settings.os == "Windows":
    #        self.cpp_info.libs = ["OpenAL32", 'winmm']
    #    else:
    #        self.cpp_info.libs = ["openal"]
    #    if self.settings.os == 'Linux':
    #        self.cpp_info.libs.extend(['dl', 'm'])
    #    elif self.settings.os == 'Macos':
    #        frameworks = ['AudioToolbox', 'CoreAudio']
    #        for framework in frameworks:
    #            self.cpp_info.exelinkflags.append("-framework %s" % framework)
    #        self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
    #    self.cpp_info.includedirs = ["include", "include/AL"]
    #    if not self.options.shared:
    #        self.cpp_info.defines.append('AL_LIBTYPE_STATIC')
