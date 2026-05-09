import uuid
import json
import zipfile
import time

from pathlib import Path

prefix = "[PACKER]"

st = time.time()

def pack_map(level, sound_files, atlas, map_path, start_time):
    '''Pack map into a geb file'''

    st = start_time
    generate_level_json(level, atlas)
    generate_geb_archive(sound_files, map_path)
    tidy_files()

def generate_level_json(level, atlas):
    '''Create level json file.'''

    print(prefix, "Generating json..")

    data = {}
    map_id = uuid.uuid1()

    data["map_id"] = str(map_id)
    data["atlas"] = atlas
    data["entities"] = []

    print(prefix, "Meta data added to json")

    for entity in level.entities:
        ent = {}
        for kvp in entity.keyPairs:
            ent[kvp] = entity.keyPairs[kvp]
        
        ent["faces"] = []
        for brush in entity.brushes:
            for face in brush.faces:
                face_dict = {}
                face_dict["vertex"] = [tuple(float(v) for v in vert) for vert in face.vertex]
                face_dict["triangles"] = [*face.tri]
                face_dict["texture"] = face.texture

                ent["faces"].append(face_dict)
        
        data["entities"].append(ent)

        print(prefix, f"Entity [{entity.keyPairs["classname"]}] added to json.")

    with open("level.json", "w") as js:
        json.dump(data, js, indent=4)

    print(prefix, "Json created.")

def generate_geb_archive(sound_files, map_file):
    '''Create a zip archive with the .geb extention and copy needed files over.'''

    map_name = f"{Path(map_file).stem}.geb"

    print(prefix, f"Compiing {map_name}")

    with zipfile.ZipFile(map_name, "w") as geb:
        geb.write("level.json")
        geb.write("atlas.png")
        #geb.write(PCOL) - wit until this is set up
        for sound in sound_files:
            geb.write(sound, arcname=f"/sound/{Path(sound).name}")

    print(prefix, f"\033[1m\033[92mMap compiled! ({"{:.1f}".format(time.time() - st)}s)\033[0m")

def tidy_files():
    '''Deletes temporary files after they are needed.'''

    print(prefix, "Cleaning up.")

    if Path("atlas.png").exists():
        Path("atlas.png").unlink()

    if Path("level.json").exists():
        Path("level.json").unlink()