import vtk
import sys

'''
dat = sys.argv[1]
grad = sys.argv[2]
'''
#set windows, renderer, and interactor

window = vtk.vtkRenderWindow()
renderer = vtk.vtkRenderer()
window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

#set mappers
mapper = vtk.vtkDataSetMapper()
act = vtk.vtkActor()


class Slider:
	def __init__(self, min, max, name, posx1, posx2, posy1, posy2):
		self.SliderRepres = vtk.vtkSliderRepresentation2D()
		self.min = min #ImageViewer.GetSliceMin()
		self.max = max #ImageViewer.GetSliceMax()
		self.SliderWidget = vtk.vtkSliderWidget()
		self.x1 = posx1
		self.x2 = posx2
		self.y1 = posy1
		self.y2 = posy2
		self.name = name
	
	def vtkSliderCallback2(self, obj, event):
	    sliderRepres = obj.GetRepresentation()
	    isoval = sliderRepres.GetValue()
	    print "Position ",isoval
	
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
		self.SliderWidget.AddObserver("EndInteractionEvent", self.vtkSliderCallback2)

xslider = Slider(0, 255, "x-plane", 0.2, 0.9, 0.8, 0.9)
xslider.create()

yslider = Slider(0, 255, "y-plane", 0.1, 0.9, 0.1, 0.1)
yslider.create()

zslider = Slider(0, 255, "z-plane", 0.9, 0.1, 0.9, 0.9)
zslider.create()

gradminslider = Slider(0, 255, "gradient min", 0.2, 0.2, 0.8, 0.2)
gradminslider.create()

gradmaxslider = Slider(0, 255, "gradient max", 0.2, 0.1, 0.8, 0.1)
gradmaxslider.create()


interactor.Initialize()
window.Render()
interactor.Start()