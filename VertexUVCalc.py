import MapClasses
import numpy as np


def calculate_uv_per_vertex(level) -> MapClasses.Map:
    '''Calculate the uv vector of each vertex in level.'''

    for entity in level.entities:
        if len(entity.brushes) == 0:
            continue
        for brush in entity.brushes:
            for face in brush.faces:

                face.vertex = [calculate_uv(vert, face) for vert in face.vertex]

    return level

def calculate_uv(vert, face) -> tuple:
    '''Calculate the uv of the given vertex.'''
    
    vertex = (vert[0], vert[1], vert[2])

    u = (face.u[0], face.u[1], face.u[2]) 
    v = (face.v[0], face.v[1], face.v[2])
    
    #scales
    su = face.uv_scale[0]
    sv = face.uv_scale[1]

    #offsets
    ou = face.u[3]
    ov = face.v[3]

    #texture width and height    
    w = h = float(255)

    tu = ((np.dot(vertex, u) / w) / su) + (ou / w)
    tv = ((np.dot(vertex, v) / h) / sv) + (ov /h) 

    return (*vert, tu, tv)