from cpt.packager import ConanMultiPackager

# openal:shared=True -o flac:shared=True -o vorbis:shared=True -o
# ogg:shared=True -o flac:shared=True -o shared=True -o dynload=False

def add_build(builder, shared_library, shared_dependencies):
    dynload = False
    if shared_dependencies == "dynload":
        dynload = True
        shared_dependencies = True
    builder.add(settings={"arch": "x86_64",
                          "build_type": "Release"},
                options={"openal:shared": True,
                         "flac:shared": shared_dependencies,
                         "vorbis:shared": shared_dependencies,
                         "ogg:shared": shared_dependencies,
                         "mpg123:shared": shared_dependencies,
                         "alure:shared": shared_library,
                         "alure:dynload": dynload})


if __name__ == "__main__":
    builder = ConanMultiPackager()
    for shared_library in [True, False]:
        for shared_dependencies in ["dynload", True, False]:
            add_build(builder, shared_library, shared_dependencies)
    builder.run()
