import vtk
import sys


dat = sys.argv[1]
grad = sys.argv[2]

isodict = {'bone': 1100, 'brain': 1057, 'face': 800}
smallthresh = [[10000, 100000], [1000,10000], [0,800]]

#set windows, renderer, and interactor

window = vtk.vtkRenderWindow()

window.SetAlphaBitPlanes(1)
window.SetMultiSamples(0)
renderer = vtk.vtkRenderer()

renderer.SetUseDepthPeeling(1)
renderer.SetMaximumNumberOfPeels(0)
renderer.SetOcclusionRatio(0.1)

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


class isosurface:
	def __init__(self, isoval, data, gradient):
		self.filt = vtk.vtkContourFilter()
		self.iso = isoval
		self.dat = data
		self.grad = gradient

	def filter(self):
		self.filt.SetInputData(self.dat.GetOutput())
		self.filt.SetValue(0, 1071)
		self.filt.Update()


class setthreshold:
	def __init__(self, values, data):
		self.threshold = vtk.vtkThreshold()
		self.g = data
		self.setval = values
		self.setthresh()

	def setthresh(self):
		self.threshold.SetInputConnection(self.g.GetOutputPort())
		self.threshold.ThresholdBetween(self.setval[0], self.setval[1])
		self.threshold.Update()

#clipping plane
# set imp func
plane = vtk.vtkPlane()
plane.SetNormal(-1.0,-1.0,-1.0)

clipx = 1.0
clipy = -1.0
clipz = -1.0 





# gradint threshold
thresh = vtk.vtkThreshold()
thresh.SetInputConnection(gradient.GetOutputPort())
thresh.ThresholdBetween(tmin, tmax)
thresh.Update()

# isosurfaces
#isosurface = vtk.vtkContourFilter()
#isosurface.SetInputConnection(data.GetOutputPort())
#isosurface.SetValue(0, 1071)
#isosurface.Update()
isolist = []
for k, v in isodict.iteritems():
	k = isosurface(v, data, gradient)
	k.filter()
	k.filt.Update()
	isolist.append(k.filt)

# gradient mag probe

isosurflist = []
for isoob in isolist:
	probe = vtk.vtkProbeFilter()
	probe.SetInputConnection(isoob.GetOutputPort()) #geometric 
	probe.SetSourceConnection(thresh.GetOutputPort()) #filter
	probe.Update()
	isosurflist.append(probe)



# set clipper
clippols = []
for each in isosurflist:
	clipper = vtk.vtkClipPolyData()
	clipper.SetInputConnection(probe.GetOutputPort())
	clipper.SetClipFunction(plane)
	clipper.InsideOutOn()
	clipper.Update()
	clippols.append(clipper)


mriColor = vtk.vtkColorTransferFunction()
mriColor.AddHSVPoint(0, 0, .27, .92)
mriColor.AddHSVPoint(1000, 1, .75, .92)
mriColor.AddHSVPoint(10000, 0, 0, 1)
mapper1 = vtk.vtkPolyDataMapper()
mapper1.SetInputConnection(clippols[0].GetOutputPort())
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(clippols[1].GetOutputPort())
mapper.SetInputConnection(clippols[2].GetOutputPort())
mapper.SetLookupTable(mriColor)
mapper1.SetLookupTable(mriColor)
mapper2.SetLookupTable(mriColor)


act2 = vtk.vtkActor()
act2.SetMapper(mapper1)
act3 = vtk.vtkActor()
act3.SetMapper(mapper2)
act.SetMapper(mapper)
renderer.AddActor(act)
renderer.AddActor(act2)
renderer.AddActor(act3)
#tada~

'''
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

'''

interactor.Initialize()
window.Render()
interactor.Start()
