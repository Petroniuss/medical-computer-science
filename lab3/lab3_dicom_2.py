import vtk

# --- source: read data
dir = 'mr_brainixA'
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir)
reader.Update()

# filter
iso_value = 100
iso_maximum_value = 1000
iso_min_value = 0
contour = vtk.vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetValue(0, iso_value)

color_tf = vtk.vtkColorTransferFunction()
color_tf.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(0.9, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(1.0, 1.0, 0.937, 0.859)

# mapper
contourMapper = vtk.vtkPolyDataMapper()
contourMapper.SetColorModeToMapScalars()
contourMapper.SetLookupTable(color_tf)
contourMapper.SetInputConnection(contour.GetOutputPort())
contourMapper.SetScalarRange(0.0, 1.2)

# actor
contourActor = vtk.vtkActor()
contourActor.SetMapper(contourMapper)

# --- renderer
ren1 = vtk.vtkRenderer()
ren1.AddActor(contourActor)

# --- window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(800 * 2, 600 * 2)

# --- interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


class FrameISOCallback(object):
    def __init__(self, actor, renWin):
        self.renWin = renWin
        self.actor = actor

    def __call__(self, caller, ev):
        value = caller.GetSliderRepresentation().GetValue()
        contour.SetValue(0, value)
        self.renWin.Render()


isoSliderRep = vtk.vtkSliderRepresentation2D()
isoSliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
isoSliderRep.GetPoint1Coordinate().SetValue(.7, .1)
isoSliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
isoSliderRep.GetPoint2Coordinate().SetValue(.9, .1)
isoSliderRep.SetMinimumValue(iso_min_value)
isoSliderRep.SetMaximumValue(iso_maximum_value)
isoSliderRep.SetValue(1)
isoSliderRep.SetTitleText("iso")

isoSlider = vtk.vtkSliderWidget()
isoSlider.SetInteractor(iren)
isoSlider.SetRepresentation(isoSliderRep)
isoSlider.SetAnimationModeToAnimate()
isoSlider.EnabledOn()
isoSlider.AddObserver('EndInteractionEvent', FrameISOCallback(contourActor, renWin))

# --- run
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
