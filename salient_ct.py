import vtk
import sys

class dataProcessor():
	def __init__(self, fname):
		self.filename = fname
		self.generic_reader = vtk.vtkDataSetReader()
		self.filter = vtk.vtkContourFilter()
		self.filter2 = vtk.vtkContourFilter()
		self.filter3 = vtk.vtkContourFilter()
		self.filter4 = vtk.vtkContourFilter()
		self.window = vtk.vtkRenderWindow()
		self.renderer = vtk.vtkRenderer()
		self.actor = vtk.vtkActor()
		self.actor2 = vtk.vtkActor()
		self.actor3 = vtk.vtkActor()
		self.actor4 = vtk.vtkActor()
		self.interactor = vtk.vtkRenderWindowInteractor()
		self.mapper = vtk.vtkPolyDataMapper()
		self.mapper2 = vtk.vtkPolyDataMapper()
		self.mapper3 = vtk.vtkPolyDataMapper()
		self.mapper4= vtk.vtkPolyDataMapper()
		self.Slider = vtk.vtkSliderRepresentation2D()
		self.SliderWidget = vtk.vtkSliderWidget()

	
	def initialize(self):
		self.generic_reader.SetFileName(self.filename)
		self.generic_reader.Update()
		return self.generic_reader

	def extractPolyData1(self):
		self.filter.SetInputData(self.initialize().GetOutput())
		self.filter.SetValue(0, 2080)
		self.filter.Update()
		return self.filter

	def extractPolyData2(self):
		self.filter2.SetInputData(self.initialize().GetOutput())
		self.filter2.SetValue(0, 4524)
		self.filter2.Update()
		return self.filter2

	def extractPolyData3(self):
		self.filter3.SetInputData(self.initialize().GetOutput())
		self.filter3.SetValue(0, 15000)
		self.filter3.Update()
		return self.filter3

	def extractPolyData4(self):
		self.filter4.SetInputData(self.initialize().GetOutput())
		self.filter4.SetValue(0, 35000)
		self.filter4.Update()
		return self.filter4


	def render(self):
		# depth peeling
		self.mapper.SetInputConnection(self.extractPolyData1().GetOutputPort())
		self.mapper2.SetInputConnection(self.extractPolyData2().GetOutputPort())
		self.mapper3.SetInputConnection(self.extractPolyData3().GetOutputPort())
		self.mapper4.SetInputConnection(self.extractPolyData4().GetOutputPort())
		self.actor.SetMapper(self.mapper)
		self.actor2.SetMapper(self.mapper2)
		self.actor3.SetMapper(self.mapper3)
		self.actor4.SetMapper(self.mapper4)
		self.renderer.AddActor(self.actor)
		self.renderer.AddActor(self.actor2)
		self.renderer.AddActor(self.actor3)
		self.renderer.AddActor(self.actor4)
		self.window.AddRenderer(self.renderer)
		self.renderer.SetUseDepthPeeling(1)
		self.renderer.SetMaximumNumberOfPeels(100)
		self.renderer.SetOcclusionRatio(0.01)
		self.window.SetMultiSamples(0)
		self.window.SetAlphaBitPlanes(1)
		self.interactor.SetRenderWindow(self.window)
		
		print(self.renderer.GetLastRenderingUsedDepthPeeling())
		if (self.renderer.GetLastRenderingUsedDepthPeeling()):
			print("depth peeling was used")
		else:
   			print("depth peeling was not used (alpha blending instead)")

		
		

		



	def start(self):
		self.interactor.Initialize()
		self.interactor.Start()



dp = dataProcessor(sys.argv[1])
dp.render()
dp.start()