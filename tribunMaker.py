"""
Generator bentuk tribun berdasarkan input 1(satu) garis panduan baris pertama tribun.
    Inputs:
        _inputCrv: Input hanya 1(satu) garis panduan untuk tribun (harus Curve).
        _flip : Ubah orientasi tribun.
        _stepTribun : Lebar step tribun dalam angka non-desimal (integer).
        _riserTribun : Tinggi step tribun dalam angka non-desimal (integer).
        _jlhBaris : Jumlah baris tribun.
        _jlhJalur : Jumlah jalur sirkulasi tribun.
        _lbrJalur : Lebar jalur sirkulasi tribun.
        _end: Jika baris terakhir adalah jalur eksit.
    Output:
        step: Output list elemen geometri horisontal tribun.
        riser: Output list elemen geometri vertikal tribun.
        outputCrvs_: Output list garis panduan pembentuk tribun.
"""

ghenv.Component.Name = "TribunMaker3D v.0.0.1"
ghenv.Component.NickName = 'u/ Teladan'
ghenv.Component.Message = "0.0.1"

import rhinoscriptsyntax as rs
import ghpythonlib as gh
import itertools

#buat function untuk multiplikasi baris.
def RowSeries(row, row_count):
    list = []
    for i in range(0, int(row_count)):
        next_row = i * row
        list.append(next_row)
    
    return list

#buat function untuk pengelompokan grup baris.
def partition( list, size):
    for i in range(0, len(list),size):
        yield list[i : i+size]

#buat function untuk input data tinggi step ke tiap baris.
def AddRow3D(curve, widths, heights, flip, riser):
    plane = rs.WorldXYPlane()
    rowWidths = []
    rowHeights = []
    rowSteps = []
    rowRisers = []
    
    #tambahkan opsi untuk flip.
    if flip == 1 :
        flipped = gh.components.FlipCurve(curve)
        flippedcurve = flipped[0]
    else :
        flippedcurve = curve
    
    #tambahkan ukuran step
    for i in range(1, len(widths)) :
        offset = gh.components.OffsetCurve(flippedcurve, widths[i], plane, 1)
        rowWidths.append(offset)
        
    rowWidths.insert(0, curve)
    
    #tambahkan ukuran riser
    for i in range(0, len(rowWidths)):
        rowHeight = rs.CopyObject(rowWidths[i], [0,0,heights[i]])
        rowHeights.append(rowHeight)
    
    #tambahkan step dengan sweep ke offset.
    resultStep = []
    for i in range(0, (len(rowWidths)-1)):
        addStep = rs.AddLoftSrf(rowWidths[i:i+2], None, None, 0, 0, False)
        resultStep.append(addStep)
    
    collectSteps = gh.treehelpers.list_to_tree(resultStep)
    flattenSteps = gh.components.FlattenTree(collectSteps, 0)
    
    #pindahkan masing2 steps ke tinggi yg benar.
    for i in range(0, (len(rowWidths)-1)):
        copyStep = rs.CopyObject(flattenSteps[i], [0,0,heights[i]])
        rowSteps.append(copyStep)

    #tambahkan riser dengan extrusion ke bawah.
    for i in range(1, len(rowHeights)):
        endPtV1 = rs.CurveEndPoint(rowHeights[i])
        endPtV2 = rs.CopyObject(endPtV1, [0,0,-abs(riser)])
        pathR = rs.AddLine(endPtV1, endPtV2)
        addRiser = rs.ExtrudeCurve(rowHeights[i], pathR)
        rowRisers.append(addRiser)
    
    #buang curve pertama supaya tidak duplikat dengan input curve.
    rowHeights.pop(0)
    
    return rowSteps, rowRisers, rowHeights

# berikan opsi ada atau tidaknya path.
if _jlhJalur >= 1:
    # proses jumlah baris tribun
    row_V = RowSeries(_riserTribun, _jlhBaris + _jlhJalur)
    row_H = RowSeries(_stepTribun, _jlhBaris)
    
    # tambahkan jalur sirkulasi ke dalam tribun.
    insert_path = int(len(row_H) / _jlhJalur)
    rowList = list(partition(row_H, insert_path))
    
    for i in range(0, len(rowList)):
        path = (rowList[i][-1] + _lbrJalur * (i+1))
        rowList[i].append(path)
        for j in range(0, len(rowList[i])-1):
            rowList[i][j] = rowList[i][j] + _lbrJalur*i
    
    rowFixed = list(itertools.chain(*rowList))
else :
    row_V = RowSeries(_riserTribun, _jlhBaris)
    rowFixed = RowSeries(_stepTribun, _jlhBaris)

# tambahkan opsi untuk jalur sirkulasi pada baris terakhir.
if _jlhJalur >= 1 and _end == 0:
    rowFixed.pop(-1)
    row_V.pop(-1)
elif _jlhJalur == 0 and _end == 1:
    pass
else :
    pass

step, riser, outputCrvs_ = AddRow3D(_inputCrv, rowFixed, row_V, _flip, _riserTribun)