import vtk

# --- source: read data
dir = 'mr_brainixA'
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir)
reader.Update()

def make_opacity_function(point_value):
    opacity_f = vtk.vtkPiecewiseFunction()
    opacity_f.AddPoint(0, 0.0)
    opacity_f.AddPoint(point_value, 0.2)
    opacity_f.AddPoint(1000, 0.8)

    return opacity_f

def make_color_function(p):
    color_function = vtk.vtkColorTransferFunction()
    color_function.SetColorSpaceToHSV()
    color_function.AddHSVPoint(0, 0.0, 0.0, 0.0)
    color_function.AddHSVPoint(p, 0.0, 0.0, 0.0)
    color_function.AddHSVPoint(128, 0.0, 0.0, 1.0)
    color_function.AddHSVPoint(255, 0.0, 0.0, 1.0)

    return color_function


# Create transfer mapping scalar value to opacity.
init_point = 256.
opacity_function = make_opacity_function(127)

# Create transfer mapping scalar value to color.
color_function = make_color_function(127)

volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(color_function)
volume_property.SetScalarOpacity(opacity_function)
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()

# mapper
mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# --- actor: imageActor (displays 2D images)
actor = vtk.vtkVolume()
actor.SetMapper(mapper)
actor.SetProperty(volume_property)

# --- renderer
ren1 = vtk.vtkRenderer()
ren1.AddActor(actor)

# --- window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(800 * 2, 600 * 2)

# --- interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# --- slider to change frame: callback class, sliderRepresentation, slider
class FrameCallback(object):
    def __init__(self, actor, renWin):
        self.renWin = renWin
        self.actor = actor

    def __call__(self, caller, ev):
        value = caller.GetSliderRepresentation().GetValue()
        # actor.GetProperty().SetColor(make_color_function(value))
        actor.GetProperty().SetScalarOpacity(make_opacity_function(value))
        self.renWin.Render()


sliderRep = vtk.vtkSliderRepresentation2D()
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(.7, .1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(.9, .1)
sliderRep.SetMinimumValue(0)
sliderRep.SetMaximumValue(1000)
sliderRep.SetValue(init_point)
sliderRep.SetTitleText("transfer function")

slider = vtk.vtkSliderWidget()
slider.SetInteractor(iren)
slider.SetRepresentation(sliderRep)
slider.SetAnimationModeToAnimate()
slider.EnabledOn()
slider.AddObserver('EndInteractionEvent', FrameCallback(actor, renWin))

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
