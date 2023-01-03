import rhinoscriptsyntax as rs
import ghpythonlib as gh

#buat variabel utk input tebal balok.
beam_depth = rs.VectorScale([0,0,-1], round(_depth, 3))

#join semua surface terpisah dari input geometri tribun.
join_faces = rs.JoinSurfaces(_tribun3D)

#proyeksikan garis grid pada geometri tribun.
project_crv = rs.ProjectCurveToSurface(_inputGrid, join_faces, [0,0,1])

#explode hasil proyeksi grid menjadi segmentasi terpisah.
list_of_crvs = rs.ExplodeCurves(project_crv)
list_of_crvs.pop(0)

#deteksi ukuran step dan path pada input geometri tribun.
riser = round(rs.CurveLength(list_of_crvs[1]), 3)
step = round(rs.CurveLength(list_of_crvs[2]), 3)

#generate titik untuk membentuk profil sisi bawah balok.
connector_pts = []

for crv in list_of_crvs:
    check_length = round(rs.CurveLength(crv), 3)
    if check_length == step :
        length = step
        startPt = rs.CurveStartPoint(crv)
        endPt = rs.CurveEndPoint(crv)
        path = rs.VectorScale(rs.VectorCreate(startPt, endPt), (_depth / length))
        new_Pt = rs.CopyObject(rs.CurveStartPoint(crv), rs.VectorAdd(beam_depth, path))
        connector_pts.append(new_Pt)
    elif check_length > step :
        length = round(rs.CurveLength(crv), 3)
        startPt = rs.CurveStartPoint(crv)
        endPt = rs.CurveEndPoint(crv)
        path1 = rs.VectorScale(rs.VectorCreate(startPt, endPt), (_depth / length))
        path2 = rs.VectorScale(rs.VectorCreate(startPt, endPt), ((_depth + step) / length))
        new_Pt1 = rs.CopyObject(rs.CurveStartPoint(crv), rs.VectorAdd(beam_depth, path1))
        new_Pt2 = rs.CopyObject(rs.CurveEndPoint(crv), rs.VectorAdd(beam_depth, path2))
        connector_pts.append(new_Pt1)
        connector_pts.append(new_Pt2)

connector_pts = connector_pts[1 : -1]
connector_pts.insert(0, rs.CopyObject(rs.CurveStartPoint(list_of_crvs[0]), beam_depth))
connector_pts.insert(len(connector_pts), rs.CopyObject(rs.CurveEndPoint(list_of_crvs[-1]), beam_depth))

beam_top = rs.JoinCurves(list_of_crvs)
beam_bottom = rs.AddPolyline(connector_pts)
beam_cap1 = rs.AddLine(rs.CurveStartPoint(beam_top), rs.CurveStartPoint(beam_bottom))
beam_cap2 = rs.AddLine(rs.CurveEndPoint(beam_top), rs.CurveEndPoint(beam_bottom))

beam = rs.AddPlanarSrf([beam_top, beam_bottom, beam_cap1, beam_cap2])