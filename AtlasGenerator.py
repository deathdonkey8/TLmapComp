import math
import ErrorTable
from PIL import Image


prefix = "[ATLAS]"
Atlas = {}
texture_resolution = 255

def generate_atlas(level, texture_folder):
    unq_tex = list_required_textures(level)
    make_atlas_texture(unq_tex, texture_folder)
    return Atlas

def list_required_textures(level) -> list[str]:
    unique_textures = []
    for entity in level.entities:
        if len(entity.brushes) == 0:
            continue
        for brush in entity.brushes:
            if len(brush.faces) == 0:
                continue
            for face in brush.faces:
                if face.texture not in unique_textures:
                    unique_textures.append(face.texture)
    return unique_textures

def make_atlas_texture(unique_textures, texture_folder):
    if len(unique_textures) > 256:
        print(ErrorTable.e3)
        return None #Max textuyre check

    atlas_width = min(len(unique_textures), 16) * 255
    atlas_height = math.ceil(len(unique_textures) / 16) * 255
    atlas_image = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))

    for index, texture in enumerate(unique_textures):
        img_path = texture_folder / f"{texture}.png"
        if not img_path.exists():
            print(ErrorTable.e0, img_path)
            continue

        print(prefix + f" opening {img_path}")
        img = Image.open(img_path)
        img = img.resize((255, 255), resample=Image.LANCZOS)

        row = index // 16
        column = index % 16

        paste_x = column * 255
        paste_y = row * 255

        atlas_image.paste(img, (paste_x, paste_y))
        Atlas[texture] = (paste_x, paste_y)

    atlas_image.save("atlas.png")
    print(prefix, "Atlas Created.")

