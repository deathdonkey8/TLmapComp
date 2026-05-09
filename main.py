import time
import MapClasses
import Parser
import PlaneIntersection
import DisplayTest
import AtlasGenerator
import SoundCollector
import VertexUVCalc
import Packer

from pathlib import Path

level = MapClasses.Map()
map_path = Path("~/Documents/test3.map").expanduser()
textureFolder = Path("~/Documents/Trenchbroom/WANKER/Textures/").expanduser()
soundFolder = Path("~/Documents/Trenchbroom/WANKER/Sounds/").expanduser()

sound_files = []
atlas = {}

start_time = time.time()

def main():
    level = Parser.parse(map_path)
    level = PlaneIntersection.intersect(level)
    level = VertexUVCalc.calculate_uv_per_vertex(level)
    sound_files = SoundCollector.get_sound_files(level, soundFolder)
    atlas = AtlasGenerator.generate_atlas(level, textureFolder)
    Packer.pack_map(level, sound_files, atlas, map_path, start_time)
    #DisplayTest.export_to_obj(level)


if __name__ == "__main__":
    main()