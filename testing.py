import vtk
import sys

fname = sys.argv[1]

filename = fname
generic_reader = vtk.vtkDataSetReader()
filter1 = vtk.vtkContourFilter()
filter2 = vtk.vtkContourFilter()
filter3 = vtk.vtkContourFilter()
filter4 = vtk.vtkContourFilter()


actor = vtk.vtkActor()
actor2 = vtk.vtkActor()
actor3 = vtk.vtkActor()
actor4 = vtk.vtkActor()
interactor = vtk.vtkRenderWindowInteractor()
mapper = vtk.vtkPolyDataMapper()
mapper2 = vtk.vtkPolyDataMapper()
mapper3 = vtk.vtkPolyDataMapper()
mapper4= vtk.vtkPolyDataMapper()
Slider = vtk.vtkSliderRepresentation2D()
SliderWidget = vtk.vtkSliderWidget()

	
generic_reader.SetFileName(filename)
generic_reader.Update()


filter1.SetInputData(generic_reader.GetOutput())
filter1.SetValue(0, 2080)
filter1.Update()

filter2.SetInputData(generic_reader.GetOutput())
filter2.SetValue(0, 4524)
filter2.Update()


filter3.SetInputData(generic_reader.GetOutput())
filter3.SetValue(0, 15000)
filter3.Update()



filter4.SetInputData(generic_reader.GetOutput())
filter4.SetValue(0, 35000)
filter4.Update()



renderer = vtk.vtkRenderer()
renderer.SetUseDepthPeeling(1)
renderer.SetAlphaBitPlanes(1)
renderer.SetMultiSamples(0)
renderer.SetMaximumNumberOfPeels(20)
renderer.SetOcclusionRatio(0.002)



# maps
# add actor
mapper.SetInputConnection(filter1.GetOutputPort())
mapper2.SetInputConnection(filter2.GetOutputPort())
mapper3.SetInputConnection(filter3.GetOutputPort())
mapper4.SetInputConnection(filter4.GetOutputPort())
actor.SetMapper(mapper)
actor2.SetMapper(mapper2)
actor3.SetMapper(mapper3)
actor4.SetMapper(mapper4)


renderer.AddActor(actor)
renderer.AddActor(actor2)
renderer.AddActor(actor3)
renderer.AddActor(actor4)

window = vtk.vtkRenderWindow()
window.SetMultiSamples(0)
window.SetAlphaBitPlanes(1)



window.AddRenderer(renderer)



#set render window


print(renderer.GetLastRenderingUsedDepthPeeling())
if (renderer.GetLastRenderingUsedDepthPeeling()):
	print("depth peeling was used")
else:
   	print("depth peeling was not used (alpha blending instead)")

interactor.SetRenderWindow(window)
interactor.Start()


