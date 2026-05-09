
def export_to_obj(level):
    '''Export to OBJ format'''

    filename = "level.obj"

    with open(filename, 'w') as obj:
        
        vertex_index = 1
        
        for entity in level.entities:
            for brush in entity.brushes:
                for face in brush.faces:
                    vertices = face.vertex
                    
                    if len(vertices) < 3:
                        continue
                    
                    vertex_start = vertex_index
                    for vert in vertices:
                        obj.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
                        vertex_index += 1
                    
                    #fan method
                    num_verts = len(vertices)
                    for i in range(1, num_verts - 1):
                        v0 = vertex_start
                        v1 = vertex_start + i
                        v2 = vertex_start + i + 1
                        obj.write(f"f {v0} {v1} {v2}\n")
    
    print(f" Exported to {filename}")