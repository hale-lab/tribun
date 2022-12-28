import rhinoscriptsyntax as rs
import ghpythonlib as gh

#buat variabel utk input tebal balok.
beam_depth = rs.VectorScale([0,0,-1], float(_depth))

#join semua surface terpisah dari input geometri tribun.
join_faces = rs.JoinSurfaces(_tribun3D)

#proyeksikan garis grid pada geometri tribun.
beam_top = rs.ProjectCurveToSurface(_inputGrid, join_faces, [0,0,1])

#explode hasil proyeksi grid menjadi segmentasi terpisah.
list_of_crvs = rs.ExplodeCurves(beam_top)

#deteksi ukuran step dan path pada input geometri tribun.
path = float(rs.CurveLength(list_of_crvs[1]))
step = float(rs.CurveLength(list_of_crvs[3]))

#generate titik untuk membentuk profil sisi bawah balok.
connector_pts = []

for crv in list_of_crvs:
    check_length = float(rs.CurveLength(crv))
    if check_length >= float(_lbrJalur - 0.01):
        move_crv = rs.CopyObject(crv, beam_depth)
        startPt = rs.CurveStartPoint(move_crv)
        connector_pts.append(startPt)

        endPt = rs.CurveEndPoint(move_crv)
        resize_path = rs.VectorScale(rs.VectorCreate(startPt, endPt), float(step/path))
        movePt = rs.CopyObject(endPt, resize_path)
        connector_pts.append(movePt)

#hilangkan titik terakhir pada list titik connector.
connector_pts.pop(-1)

#hilangkan riser terakhir pada profil atas
beam_top = rs.JoinCurves(list_of_crvs[1:])

#gabung semua curve untuk membentuk profil bawah.
beam_bottom = rs.JoinCurves([rs.AddPolyline(connector_pts, None),rs.CopyObject(list_of_crvs[-1], beam_depth)], True, None)

#buat cap utk menutup profil atas dan bawah menjadi closed curve.
beam_cap1 = rs.AddLine(rs.CurveStartPoint(beam_top), rs.CurveStartPoint(beam_bottom))
beam_cap2 = rs.AddLine(rs.CurveEndPoint(beam_top), rs.CurveEndPoint(beam_bottom))

#buat planar surface dari profile edge.
beam = rs.AddPlanarSrf([beam_top, beam_bottom, beam_cap1, beam_cap2])