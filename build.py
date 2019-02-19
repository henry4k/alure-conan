from cpt.packager import ConanMultiPackager

# openal:shared=True -o flac:shared=True -o vorbis:shared=True -o
# ogg:shared=True -o flac:shared=True -o shared=True -o dynload=False

if __name__ == "__main__":
    builder = ConanMultiPackager(
        options=["openal:shared=True",
                 "flac:shared=True",
                 "vorbis:shared=True",
                 "ogg:shared=True",
                 "alure:shared=True",
                 "alure:dynload=False"])
    builder.add_common_builds()
    builder.run()
