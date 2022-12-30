import rhinoscriptsyntax as rs
import ghpythonlib as gh

transit_crv = _inputCrvs[-1]
wall = rs.CopyObject(transit_crv, [0, 0, _riserTransit - _riserTribun])

midPt = rs.CurveMidPoint(transit_crv)
copy_midPt = rs.CurveMidPoint(wall)



step = rs.OffsetCurve(wall, (-10000, -10000, 0), _stepTribun + 0.15)
riser = rs.CopyObject(step, [0, 0, _riserTribun])

transit_wall = rs.ExtrudeCurve(transit_crv, rs.AddLine(midPt,copy_midPt))
transit_riser = rs.ExtrudeCurve(step, rs.AddLine(rs.CurveMidPoint(step), rs.CurveMidPoint(riser)))
transit_step = gh.components.FlattenTree(gh.treehelpers.list_to_tree(rs.AddLoftSrf([wall, step], None, None, 2, 2)),0)

transit_3D = [transit_wall, transit_step, transit_riser]

transit_seat = riser
outputCrv_ = riser