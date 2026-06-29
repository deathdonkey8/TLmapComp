import MapClasses
import numpy as np

prefix = "[INTER]"

def intersect(level):
    level = calculate_normals(level)
    level = intersect_faces(level)
    return level

def calculate_normals(level) -> MapClasses.Map:
    print(prefix, "calculating plane normals...")
    for entity in level.entities:
        for brush in entity.brushes:
            for face in brush.faces:
                #converting point tuples into numpy array for crossing
                point_1 = np.array(face.plane.points[0])
                point_2 = np.array(face.plane.points[1])
                point_3 = np.array(face.plane.points[2])

                #make edges for normal calculation
                edge_1 = point_2 - point_1
                edge_2 = point_3 - point_1

                #calculate normal of plane
                face.plane.normal = np.cross(edge_1, edge_2)

                #normalize the planes normal
                magnitude = np.linalg.norm(face.plane.normal)
                if magnitude > 0:
                    face.plane.normal = face.plane.normal / magnitude

                #calculate distance: d = -(n.x*p1.x+n.y*p1.y+n.z*p1.z)
                face.plane.distance = -(
                    face.plane.normal[0]*point_1[0]+
                    face.plane.normal[1]*point_1[1]+
                    face.plane.normal[2]*point_1[2]
                )
                print(prefix, f"{face} plane normal calculated")

    return level

def intersect_faces(level) -> MapClasses.Map:
    print(prefix, "intersecting planes...")
    for entity in level.entities:
        for brush in entity.brushes:
            unique_vert = []
            for i in range(len(brush.faces)):
                for j in range(len(brush.faces)):
                    if i == j:
                        continue
                    for k in range(len(brush.faces)):
                        if k == i or k == j:
                            continue

                        vert = get_intersection(
                            brush.faces[i].plane, 
                            brush.faces[j].plane, 
                            brush.faces[k].plane
                        )

                        if vert is not None and point_inside_brush(vert, brush):
                            is_duplicate = False
                            for existing_vert in unique_vert:
                                if np.allclose(vert, existing_vert, atol=1e-4):
                                    is_duplicate = True
                                    break
    
                            if not is_duplicate:
                                unique_vert.append(vert)
                                brush.faces[i].vertex.append(vert)
                                brush.faces[j].vertex.append(vert)
                                brush.faces[k].vertex.append(vert)
        for brush in entity.brushes:
            for face in brush.faces:
                if len(face.vertex) >= 3:
                    face.vertex = sort_vertex(face.vertex, face.plane.normal)
    return level

def get_intersection(plane_1, plane_2, plane_3) -> tuple:
    n1 = np.array(plane_1.normal)
    n2 = np.array(plane_2.normal)
    n3 = np.array(plane_3.normal)

    d1 = plane_1.distance
    d2 = plane_2.distance
    d3 = plane_3.distance

    denom = np.dot(n1, np.cross(n2, n3))

    if abs(denom) < 1e-6: #catch rounding errors
        return None

    numerator = (
                d1 * np.cross(n2, n3) +
                d2 * np.cross(n3, n1) +
                d3 * np.cross(n1, n2)
                )

    intersection = -numerator / denom

    return tuple(intersection)

def sort_vertex(verticies, normal):

    if len(verticies) < 3:
        return verticies

    verticies = [np.array(v) for v in verticies]
    normal = np.array(normal)

    point_centre = np.mean(verticies, axis=0)

    def angle_from_centre(v):
        point_a = v - point_centre
        point_b = verticies[0] - point_centre

        plane_normal = np.cross(point_a, normal)
        angle = np.arctan2(np.dot(plane_normal, point_b), np.dot(point_a, point_b))
        return angle
    
    sorted_verts = sorted(verticies, key=angle_from_centre)
    
    calc_normal = np.cross(
        sorted_verts[1] - sorted_verts[0],
        sorted_verts[2] - sorted_verts[0]
    )

    if np.dot(calc_normal, normal) < 0:
        sorted_verts.reverse()

    sorted_verts.reverse()
    return [tuple(v) for v in sorted_verts]

def point_inside_brush(point, brush, epsilon=1e-5):
    p = np.array(point)

    for face in brush.faces:
        n = np.array(face.plane.normal)
        d = face.plane.distance

        # plane equation: n·p + d <= 0 (assuming inwards normals)
        if np.dot(n, p) + d < -epsilon:
            return False

    return True