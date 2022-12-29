import rhinoscriptsyntax as rs
import ghpythonlib as gh

transit_crv = _inputCrvs[-1]
transit_wall = rs.CopyObject(transit_crv, [0, 0, _riserTransit - _riserTribun])
transit_step = rs.OffsetCurve(transit_wall, (-10000, -10000, 0), _stepTribun + 0.15)
transit_riser = rs.CopyObject(transit_step, [0, 0, _riserTribun])
transit_3D = rs.AddLoftSrf([transit_crv, transit_wall, transit_step, transit_riser], None, None, 2, 2)

transit_seat = transit_step
outputCrv_ = transit_riser