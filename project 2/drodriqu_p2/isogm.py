import vtk
import sys


#set windows, renderer, and interactor

data = sys.argv[1]
grad = sys.argv[2]

try:
	optiso = float(sys.argv[3])
except:
	optiso = 1000


try:
	clipx = float(sys.argv[4])
	clipy = float(sys.argv[5])
	clipz = float(sys.argv[6])
except:
	clipx = 0
	clipy = 0
	clipz = 0




volume = vtk.vtkDataSetReader()
volume.SetFileName(data)
volume.Update()

g = vtk.vtkDataSetReader()
g.SetFileName(grad)
g.Update()


window = vtk.vtkRenderWindow()
renderer = vtk.vtkRenderer()
window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

#set mappers
mapper = vtk.vtkDataSetMapper()
act = vtk.vtkActor()
act.SetMapper(mapper)
renderer.AddActor(act)

iso = vtk.vtkContourFilter()
iso.SetInputConnection(volume.GetOutputPort())
iso.SetValue(0, optiso)
iso.Update()


# probe

probe = vtk.vtkProbeFilter()
probe.SetInputConnection(iso.GetOutputPort()) #geometric 
probe.SetSourceConnection(g.GetOutputPort()) #filter
probe.Update()



plane = vtk.vtkPlane()
plane.SetOrigin(probe.GetOutput().GetCenter())
plane.SetNormal(clipx,clipy,clipz)

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(probe.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()
clipper.Update()


mapper.SetInputConnection(clipper.GetOutputPort())
mriColor = vtk.vtkColorTransferFunction()
mriColor.AddHSVPoint(0, 0, .27, .92)
mriColor.AddHSVPoint(1000, 1, .75, .92)
mriColor.AddHSVPoint(10000, 0, 0, 1)
mapper.SetLookupTable(mriColor)


def slidex(obj, event):
    sliderRepres = obj.GetRepresentation()
    clip = sliderRepres.GetValue()
    clipx = clip
    plane.SetNormal(clipx, clipy, clipz)

def slidey(obj, event):
    sliderRepres = obj.GetRepresentation()
    clip = sliderRepres.GetValue()
    clipy = clip
    plane.SetNormal(clipx, clipy, clipz)

def slidez(obj, event):
    sliderRepres = obj.GetRepresentation()
    clip = sliderRepres.GetValue()
    clipz = clip
    plane.SetNormal(clipx, clipy, clipz)

def isoval(obj, event):
    sliderRepres = obj.GetRepresentation()
    retval = sliderRepres.GetValue()
    iso.SetValue(0, retval)

class Slider:
	def __init__(self, min, max, name, posx1, posx2, posy1, posy2, func):
		self.SliderRepres = vtk.vtkSliderRepresentation2D()
		self.min = min #ImageViewer.GetSliceMin()
		self.max = max #ImageViewer.GetSliceMax()
		self.SliderWidget = vtk.vtkSliderWidget()
		self.x1 = posx1
		self.x2 = posx2
		self.y1 = posy1
		self.y2 = posy2
		self.name = name
		self.val = 0
		self.function = func
	
	def create(self):
		self.SliderRepres.SetMinimumValue(self.min)
		self.SliderRepres.SetMaximumValue(self.max)
		self.SliderRepres.SetValue((self.min + self.max) / 2)
		self.SliderRepres.SetTitleText(self.name)
		self.SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
		self.SliderRepres.GetPoint1Coordinate().SetValue(self.x1, self.x2)
		self.SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
		self.SliderRepres.GetPoint2Coordinate().SetValue(self.y1, self.y2)
		self.SliderRepres.SetSliderLength(0.02)
		self.SliderRepres.SetSliderWidth(0.03)
		self.SliderRepres.SetEndCapLength(0.01)
		self.SliderRepres.SetEndCapWidth(0.03)
		self.SliderRepres.SetTubeWidth(0.005)
		self.SliderRepres.SetLabelFormat("%3.0lf")
		self.SliderRepres.SetTitleHeight(0.02)
		self.SliderRepres.SetLabelHeight(0.02)
		self.SliderWidget = vtk.vtkSliderWidget()
		self.SliderWidget.SetInteractor(interactor)
		self.SliderWidget.SetRepresentation(self.SliderRepres)
		self.SliderWidget.KeyPressActivationOff()
		self.SliderWidget.SetAnimationModeToAnimate()
		self.SliderWidget.SetEnabled(True)
		self.SliderWidget.AddObserver("EndInteractionEvent", self.function)

xslider = Slider(0, 10, "Sagital", 0.2, 0.9, 0.8, 0.9, slidex)
xslider.create()


yslider = Slider(0, 10, "Axial", 0.1, 0.9, 0.1, 0.1, slidey)
yslider.create()

zslider = Slider(0, 10, "Coronal", 0.9, 0.1, 0.9, 0.9, slidez)
zslider.create()

isovalslider = Slider(800, 1200, "Isovalue", 0.2, 0.8, 0.8, 0.8, isoval)
isovalslider.create()


interactor.Initialize()
window.Render()
interactor.Start()