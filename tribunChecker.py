"""
Komponen untuk validasi geometri tribun terhadap standar sudut pandangan FIFA.
    Inputs:
        _kT: Input lokasi uji (kursi penonton)
        _pL: Input target uji (garis pinggir lapangan)
    Output:
        hasilUji : Lihat hasil uji.
        testResults: Hasil uji sudut pandangan.
        viewLines : Garis lurus pandangan ke pinggir lapangan.
        eyeLevels: Tinggi posisi mata penonton.
"""

ghenv.Component.Name = "UjiSudutPandangan_FIFA"
ghenv.Component.NickName = 'u/ Teladan'
ghenv.Component.Message = "0.0.1"

import rhinoscriptsyntax as rs
import ghpythonlib as gh

def OffsetList(list):
    
    first = list[0]
    slice = list[1:]
    slice.append(first)
    
    return slice

#variabel tinggi mata dan kepala
h_mata = 0.875
delta_kepala = 0.100

#variabel lainnya
kursiTribun = _kT[:-1]
titik_mata = []
testPts = []
testResults = []
viewLines = []
eyeLevels = []
hasilUji = []
lulus = []
gagal = []


#tentukan titik terdekat antara tribun penonton ke garis lapangan.
garisLap = rs.EvaluateCurve(_pL, rs.CurveClosestPoint(_pL, kursiTribun[0]))

#buat posisi mata dan garis pandangan.
for i in range(0, len(kursiTribun)):
    copy_mata = rs.CopyObject(_kT[i],[0,0,h_mata])
    titik_mata.append(copy_mata)
    viewLine = rs.AddLine(copy_mata, garisLap)
    viewLines.append(viewLine)
    eyeLevel = rs.AddLine(kursiTribun[i], copy_mata)
    eyeLevels.append(eyeLevel)
    
viewLines_fix = OffsetList(viewLines)

#uji sudut pandangan.
for i in range(0, len(kursiTribun)):
    testPt_param = rs.CurveClosestPoint(viewLines_fix[i],titik_mata[i])
    testPt = rs.EvaluateCurve(viewLines_fix[i], testPt_param)
    testPts.append(testPt)

for i in range(0, len(kursiTribun)-1):
    testResult = rs.AddLine(titik_mata[i], testPts[i])
    testResults.append(testResult)
    
#proses hasil uji.
for i in range(0, len(testResults)):
    result = rs.CurveLength(testResults[i])
    vector = rs.VectorCreate(rs.CurveStartPoint(testResults[i]), rs.CurveEndPoint(testResults[i]))
    print(vector[2])
    if result >= delta_kepala and float(vector[2]) < 0:
        write = "sesuai standar FIFA!"
        hasilUji.append(write)
        lulus.append(write)
    else :
        write = "belum standar FIFA!"
        hasilUji.append(write)
        gagal.append(write)

print(str(len(gagal)) + " titik uji belum lulus standar FIFA dari total " + str(len(hasilUji)) + " titik uji.")