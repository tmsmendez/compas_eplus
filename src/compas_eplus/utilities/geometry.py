from compas.datastructures import Mesh


def make_box(w, l, h, spt=[0,0,0]):
    p0 = [spt[0]    , spt[1]    , spt[2]]
    p1 = [spt[0] + w, spt[1]    , spt[2]]
    p2 = [spt[0] + w, spt[1] + l, spt[2]]
    p3 = [spt[0]    , spt[1] + l, spt[2]]
    p4 = [spt[0]    , spt[1]    , spt[2] + h]
    p5 = [spt[0] + w, spt[1]    , spt[2] + h]
    p6 = [spt[0] + w, spt[1] + l, spt[2] + h]
    p7 = [spt[0]    , spt[1] + l, spt[2] + h]

    f0 = [0, 3, 2, 1]
    f1 = [4, 5, 6, 7]
    f2 = [0, 1, 5, 4]
    f3 = [1, 2, 6, 5]
    f4 = [2, 3, 7, 6]
    f5 = [3, 0, 4, 7]

    vertices  = [p0, p1, p2, p3, p4, p5, p6, p7]
    faces = [f0, f1, f2, f3, f4, f5]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    return mesh


def make_box_from_quad(quad, height):

    f0 = [0, 3, 2, 1]
    f1 = [4, 5, 6, 7]
    f2 = [0, 1, 5, 4]
    f3 = [1, 2, 6, 5]
    f4 = [2, 3, 7, 6]
    f5 = [3, 0, 4, 7]

    quad_ = [[p[0], p[1], p[2] + height] for p in quad]
    quad.extend(quad_)
    faces = [f0, f1, f2, f3, f4, f5]

    mesh = Mesh.from_vertices_and_faces(quad, faces)
    return mesh