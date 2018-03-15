import vtk
import sys


dat = sys.argv[1]
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


#set windows, renderer, and interactor

window = vtk.vtkRenderWindow()

#window.SetAlphaBitPlanes(1)
#window.SetMultiSamples(0)
renderer = vtk.vtkRenderer()

#renderer.SetUseDepthPeeling(1)
#renderer.SetMaximumNumberOfPeels(100)
#renderer.SetOcclusionRatio(0.1)

window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

#set mappers
mapper = vtk.vtkDataSetMapper()
act = vtk.vtkActor()

# set file readers and update
data = vtk.vtkDataSetReader()
data.SetFileName(dat)
gradient = vtk.vtkDataSetReader()
gradient.SetFileName(grad)
data.Update()
gradient.Update()
tmin, tmax = gradient.GetOutput().GetPointData().GetScalars().GetRange()
tmin2 = 0
tmax2 = 0

#clipping plane
# set imp func
plane = vtk.vtkPlane()
plane.SetNormal(clipx,clipy,clipz)






# gradint threshold
thresh = vtk.vtkThreshold()
thresh.SetInputConnection(gradient.GetOutputPort())
thresh.ThresholdBetween(tmin, tmax)
thresh.Update()

# isosurfaces
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(data.GetOutputPort())
isosurface.SetValue(0, optiso)
isosurface.Update()

# gradient mag probe

probe = vtk.vtkProbeFilter()
probe.SetInputConnection(isosurface.GetOutputPort()) #geometric 
probe.SetSourceConnection(thresh.GetOutputPort()) #filter
probe.Update()




# set clipper
clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(probe.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()
clipper.Update()

mriColor = vtk.vtkColorTransferFunction()
if 'small' in grad:
    mriColor.AddHSVPoint(0, 0, .27, .92)
    mriColor.AddHSVPoint(1000, 1, .75, .92)
    mriColor.AddHSVPoint(10000, 0, 0, 1)
if 'hr' in grad:
    mriColor.AddHSVPoint(1 , 0, .27, .92)
    mriColor.AddHSVPoint(20000, 1, .75, .92)
    mriColor.AddHSVPoint(30000, 0, 0, 1)


mapper.SetInputConnection(clipper.GetOutputPort())
mapper.SetLookupTable(mriColor)



act.SetMapper(mapper)
renderer.AddActor(act)


def gmax(obj, event):
    sliderRepres = obj.GetRepresentation()
    tmin = sliderRepres.GetValue()
    thresh.ThresholdBetween(tmin, tmax)
    probe.Update()

def gmin(obj, event):
    sliderRepres = obj.GetRepresentation()
    tmax = sliderRepres.GetValue()
    thresh.ThresholdBetween(tmin, tmax)
    probe.Update()
    

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
    isosurface.SetValue(0, retval)

	
# create slider class
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

gradminslider = Slider(tmin, tmax, "gradient min", 0.2, 0.2, 0.8, 0.2, gmax)
gradminslider.create()


gradmaxslider = Slider(tmin, tmax, "gradient max", 0.2, 0.1, 0.8, 0.1, gmin)
gradmaxslider.create()

isovalslider = Slider(800, 1200, "Isovalue", 0.2, 0.8, 0.8, 0.8, isoval)
isovalslider.create()



interactor.Initialize()
window.Render()
interactor.Start()
