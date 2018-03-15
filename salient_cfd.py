import vtk
import sys

class dataProcessor():
	def __init__(self, fname):
		self.filename = fname
		self.generic_reader = vtk.vtkDataSetReader()
		self.filter = vtk.vtkContourFilter()
		self.window = vtk.vtkRenderWindow()
		self.renderer = vtk.vtkRenderer()
		self.actor = vtk.vtkActor()
		self.interactor = vtk.vtkRenderWindowInteractor()
		self.mapper = vtk.vtkPolyDataMapper()
		self.Slider = vtk.vtkSliderRepresentation2D()
		self.SliderWidget = vtk.vtkSliderWidget()
		self.mriColor = vtk.vtkColorTransferFunction()
		self.cobar = vtk.vtkScalarBarActor()
		self.colorTransfer()

	
	def initialize(self):
		self.generic_reader.SetFileName(self.filename)
		self.generic_reader.Update()
		return self.generic_reader

	def extractPolyData(self):
		self.filter.SetInputData(self.initialize().GetOutput())
		self.filter.SetValue(0, 800)
		self.filter.Update()
		return self.filter


	def vtkSliderCallback(self, obj, event):
	    sliderRepres = obj.GetRepresentation()
	    isoval = sliderRepres.GetValue()
	    print "Position ",isoval
	    return self.filter.SetValue(0, isoval)

	def createIsoSlider(self):
		min = 800 #ImageViewer.GetSliceMin()
		max = 1200 #ImageViewer.GetSliceMax()
		self.Slider.SetMinimumValue(min)
		self.Slider.SetMaximumValue(max)
		self.Slider.SetValue((min + max) / 2)
		self.Slider.SetTitleText("Isovalue")
		self.Slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
		self.Slider.GetPoint1Coordinate().SetValue(0.2, 0.9)
		self.Slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
		self.Slider.GetPoint2Coordinate().SetValue(0.8, 0.9)
		self.Slider.SetSliderLength(0.02)
		self.Slider.SetSliderWidth(0.03)
		self.Slider.SetEndCapLength(0.01)
		self.Slider.SetEndCapWidth(0.03)
		self.Slider.SetTubeWidth(0.005)
		self.Slider.SetLabelFormat("%3.0lf")
		self.Slider.SetTitleHeight(0.02)
		self.Slider.SetLabelHeight(0.02)
		self.SliderWidget.SetInteractor(self.interactor)
		self.SliderWidget.SetRepresentation(self.Slider)
		self.SliderWidget.KeyPressActivationOff()
		self.SliderWidget.SetAnimationModeToAnimate()
		self.SliderWidget.SetEnabled(True)
		self.SliderWidget.AddObserver("EndInteractionEvent", self.vtkSliderCallback)

	def colorTransfer(self):
		self.mriColor.AddHSVPoint(800, 0, .27, .92)
		self.mriColor.AddHSVPoint(1057, 1, .75, .92)
		self.mriColor.AddHSVPoint(1100, 0, 0, 1)

	def colorbar(self):
		self.cobar.SetLookupTable(self.mriColor.GetLookupTable())
		self.cobar.SetOrientationToHorizontal()
		self.cobar.GetLabelTextProperty().SetColor(1,1,1)
		coord = self.cobar.GetPositionCoordinate()
		coord.SetCoordinateSystemToNormalizedViewport()
		coord.SetValue(0.1,0.05)
		self.cobar.SetWidth(.8)
		self.cobar.SetHeight(.15)



	def render(self):
		self.mapper.SetInputConnection(self.extractPolyData().GetOutputPort())
		self.mapper.SetLookupTable(self.mriColor)
		self.actor.SetMapper(self.mapper)
		self.interactor.SetRenderWindow(self.window)
		self.window.AddRenderer(self.renderer)
		self.renderer.AddActor(self.actor)
		self.renderer.AddActor(self.cobar)


	def start(self):
		self.interactor.Initialize()
		self.interactor.Start()



dp = dataProcessor(sys.argv[1])
dp.extractPolyData()
dp.render()
dp.createIsoSlider()
dp.start()