from conans import ConanFile, CMake, tools
import os


class AlureConan(ConanFile):
    name = 'alure'
    version = '1.2'
    md5 = '77cbee1d57ec4ec7d9b3ffef19e08f76' # for the .tar.gz archive
    license = 'MIT'
    author = 'henry4k <henry4k@example.org>' # TODO
    url = 'https://github.com/henry4k/alure-conan'
    homepage = 'https://kcat.strangesoft.net/alure.html'
    description = 'ALURE is a utility library to help manage common tasks with OpenAL applications'
    topics = ('audio')
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'dynload': [True, False]
    }
    default_options = 'shared=False', 'fPIC=True', 'dynload=True'
    generators = 'cmake'
    source_subfolder = 'source_subfolder'
    exports_sources = ['CMakeLists.txt',
                       'FindALURE.cmake']
    requires = (('openal/1.19.0@bincrafters/stable'),
                ('ogg/1.3.3@bincrafters/stable'),
                ('vorbis/1.3.6@bincrafters/stable'),
                ('flac/1.3.2@bincrafters/stable'))

    def source(self):
        source_url_template = 'https://kcat.strangesoft.net/alure-releases/alure-{0}.tar.gz'
        tools.get(source_url_template.format(self.version), self.md5)
        extracted_dir = 'alure-{0}'.format(self.version)
        os.rename(extracted_dir, self.source_subfolder)

        pattern = 'SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")\n'
        cmake_file = os.path.join(self.source_subfolder, 'CMakeLists.txt')
        tools.replace_in_file(cmake_file, pattern, '')

        tools.replace_in_file(os.path.join(self.source_subfolder,
                                           'cmake',
                                           'CheckFileOffsetBits.cmake'),
                              '${CMAKE_SOURCE_DIR}/cmake',
                              '${CMAKE_SOURCE_DIR}/'+self.source_subfolder+'/cmake')
    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions['BUILD_SHARED'] = 'ON' if self.options.shared else 'OFF'
        cmake.definitions['BUILD_STATIC'] = 'ON' if not self.options.shared else 'OFF'
        cmake.definitions['DYNLOAD'] = 'ON' if self.options.dynload else 'OFF'
        cmake.definitions['VORBIS'] = 'ON'
        cmake.definitions['FLAC'] = 'ON'
        cmake.definitions['SNDFILE'] = 'OFF'
        cmake.definitions['DUMB'] = 'OFF'
        cmake.definitions['MODPLUG'] = 'OFF'
        cmake.definitions['FLUIDSYNTH'] = 'OFF'
        cmake.definitions['MPG123'] = 'OFF'
        cmake.definitions['BUILD_EXAMPLES'] = 'OFF'
        cmake.definitions['INSTALL_EXAMPLES'] = 'OFF'
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy('COPYING',
                  src=self.source_subfolder,
                  dst='licenses',
                  keep_path=False)

    def package_info(self):
        self.copy('CMakeLists.txt', '.', '.')
        self.copy('FindALURE.cmake', '.', '.')
        self.cpp_info.libs = tools.collect_libs(self)
