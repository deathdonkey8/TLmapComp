from pathlib import Path
import MapClasses
import os
import re
import ErrorTable

game = "WANKER"
prefix = "[PARSER]"
level = MapClasses.Map()

pattern_kvp =  re.compile(r'\s*"([^"]+)"\s*"([^"]+)"')
pattern_header = re.compile(r'//\s*\w+:\s+(\w+)')
pattern_face = re.compile(
    r'\(\s*([-\d.eE\s]+)\s*\)'
    r'\s*\(\s*([-\d.eE\s]+)\s*\)'
    r'\s*\(\s*([-\d.eE\s]+)\s*\)'
    r'\s+(\S+)\s+'
    r'\[([-\d.eE\s]+)\]'
    r'\s+\[([-\d.eE\s]+)\]\s+'
    r'([-\d.eE]+)\s+([-\d.]+)\s+([-\d.]+)' 
)

def parse(fn: str) -> MapClasses.Map:
    '''Parse a .map file into MapClasses.Map'''
    fileName = os.path.expanduser(fn)
    fileCheck = Path(fileName).exists()

    if fileCheck is False:
        print(f"{ErrorTable.e0} @ .map")
        return

    with open(fileName, 'r') as file:
        fileContent = file.readlines()

    print(prefix, f"[{fileName}] has been loaded!")
    
    #Checks that the file is in the correct format
    if not header_check(fileContent):
        return

    print(prefix, "parsing entities...")
    level.entities = parse_entities(fileContent)

    return level

def header_check(fileContent) -> bool:
    '''Check that the map file has the header stating the format and game'''
    
    #Getting the game and format from text
    checkGame = re.search(pattern_header, fileContent[0].strip())
    checkFormat = re.search(pattern_header, fileContent[1].strip())

    if not checkGame and not checkFormat:
        print(prefix, ErrorTable.e1)
        return False
    if checkFormat.group(1) != "Valve":
        print(prefix, ErrorTable.e2)
        return False
    if checkGame.group(1) != game:
        print(prefix, ErrorTable.i0)
        return True

    print(prefix, f"map in correct format: {game} Valve")
    return True

def parse_face(line) -> MapClasses.Face:
    '''Parse faces within a brush'''
    print(line)
    face = MapClasses.Face()
    face_values = re.match(pattern_face, line)

    face.plane = MapClasses.Plane()
    normal_1 = tuple(float(value) for value in face_values.group(1).split())
    normal_2 = tuple(float(value) for value in face_values.group(2).split())
    normal_3 = tuple(float(value) for value in face_values.group(3).split())
    face.plane.points.extend([normal_1, normal_2, normal_3])

    face.texture = face_values.group(4)

    face.u = tuple(float(value) for value in face_values.group(5).split())
    face.v = tuple(float(value) for value in face_values.group(6).split())
    face.uv_scale = (float(face_values.group(8)), float(face_values.group(9)))

    return face

def parse_entities(fileContent) -> list[MapClasses.Entity]:
    '''Parse entities along with their kvp and brushes'''

    entities = []
    entity_depth = 0
    entity_count = 0
    brush_count = 0

    for line in fileContent:
        line = line.strip()

        if not line or line.startswith("//"):
            continue
        
        if line == "{" and entity_depth == 0:
            print(prefix, f"entity {entity_count} found")
            entity_depth += 1
            current_entity = MapClasses.Entity()
            continue
        elif line == "{" and entity_depth > 0:
            print(prefix, f"brush {brush_count} found")
            entity_depth += 1
            current_brush = MapClasses.Brush()
            continue
        
        elif line == "}" and entity_depth == 1:
            print(prefix, f"entity {entity_count} parsed")
            entity_depth -= 1
            brush_count = 0
            entity_count += 1
            entities.append(current_entity)
            continue
        elif line == "}" and entity_depth > 1:
            print(prefix, f"-> brush {brush_count} parsed")
            entity_depth -= 1
            brush_count += 1
            current_entity.brushes.append(current_brush)
            continue
        
        if entity_depth == 1:
            kvp = re.match(pattern_kvp, line)
            if not kvp:
                continue 
            current_entity.keyPairs[kvp.group(1)] = kvp.group(2)
        elif entity_depth > 1:
            current_brush.faces.append(parse_face(line))
    return entities
