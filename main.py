import os
import time
import MapClasses
import Parser
import PlaneIntersection
import DisplayTest
import AtlasGenerator
import SoundCollector
import VertexUVCalc
import Packer
import argparse
import ErrorTable

from pathlib import Path

level = MapClasses.Map()
#map_path = Path("~/Documents/test3.map").expanduser()
#textureFolder = Path("~/Documents/Trenchbroom/WANKER/Textures/").expanduser()
#soundFolder = Path("~/Documents/Trenchbroom/WANKER/Sounds/").expanduser()

sound_files = []
atlas = {}

start_time = time.time()

##PARSE CODE##
def valid_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(ErrorTable.e0 + f"[{path}]")
    return path

parseArgs = argparse.ArgumentParser(description="Compile map to output folder")

parseArgs.add_argument("--map",     required=True,      type=valid_path,    help="Path to map file")
parseArgs.add_argument("--tex",     required=False,     type=valid_path,    help="Path to texture folder")
parseArgs.add_argument("--out",     required=True,      type=valid_path,    help="Path to output location")
parseArgs.add_argument("--sound",   required=False,     type=valid_path,    help="Path to sound folder")


args = parseArgs.parse_args()

map_path = Path(args.map)
textureFolder = Path(args.tex) if args.tex      else None
soundFolder = Path(args.sound) if args.sound    else None
outputFolder = Path(args.out)


def main():
    level = Parser.parse(map_path)
    level = PlaneIntersection.intersect(level)
    level = VertexUVCalc.calculate_uv_per_vertex(level)
    sound_files = SoundCollector.get_sound_files(level, soundFolder)
    atlas = AtlasGenerator.generate_atlas(level, textureFolder)
    Packer.pack_map(level, sound_files, atlas, map_path, start_time, outputFolder)
    #DisplayTest.export_to_obj(level)


if __name__ == "__main__":
    main()