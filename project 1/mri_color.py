import sys
import vtk
import math

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "[filename]")
    exit()

renderer = vtk.vtkRenderer()

filename = sys.argv[1]

generic_reader = vtk.vtkDataSetReader()
generic_reader.SetFileName(sys.argv[1])
generic_reader.Update()

mrimapper = vtk.vtkDataSetMapper()
mrihypermapper = vtk.vtkDataSetMapper()

#structured
data = generic_reader.GetStructuredPointsOutput()
a,b = generic_reader.GetOutput().GetPointData().GetScalars().GetRange()



def brain():
	mriColor = vtk.vtkColorTransferFunction()
	h = 0
	s = 0
	v = 0
	step = 5
	inc = (2/(b/step))
	for i in range(int(a), int(b/2), step):
		mriColor.AddHSVPoint(i, h, s, v)
		v += inc
	for i in range(int(b/2), int(b), step):
		mriColor.AddHSVPoint(i, h, s, v)
		v -= inc
	return mriColor

def structure():
	mriColor = vtk.vtkColorTransferFunction()
	h = 0
	s = 0
	v = 0
	step = 5
	inc = (1/(b/step))
	for i in range(int(a), int(b), step):
		mriColor.AddHSVPoint(i, h, s, v)
		v += inc
	return mriColor

xmins=[0,0]
xmaxs=[1,1]
ymins=[0,0.5]
ymaxs=[0.5,1]

def mapmri():
	mrimapper.SetLookupTable(structure())
	mrimapper.SetInputConnection(generic_reader.GetOutputPort())
	scalarBar = vtk.vtkScalarBarActor()
	scalarBar.SetLookupTable(mrimapper.GetLookupTable())
	scalarBar.SetOrientationToHorizontal()
	scalarBar.GetLabelTextProperty().SetColor(1,1,1)
	coord = scalarBar.GetPositionCoordinate()
	coord.SetCoordinateSystemToNormalizedViewport()
	coord.SetValue(0.1,0.05)
	scalarBar.SetWidth(.8)
	scalarBar.SetHeight(.15)
	actor = vtk.vtkActor()
	actor.SetMapper(mrimapper)
	renderer = vtk.vtkRenderer()
	renderer.AddActor(actor)
	renderer.AddActor(scalarBar)
	renderer.SetViewport(xmins[0],ymins[0],xmaxs[0],ymaxs[0])
	return renderer

def mapmrihyper():
	mrihypermapper.SetLookupTable(brain())
	mrihypermapper.SetInputConnection(generic_reader.GetOutputPort())
	scalarBarhyper = vtk.vtkScalarBarActor()
	scalarBarhyper.SetLookupTable(mrihypermapper.GetLookupTable())
	scalarBarhyper.SetOrientationToHorizontal()
	scalarBarhyper.GetLabelTextProperty().SetColor(1,1,1)
	coordhyper = scalarBarhyper.GetPositionCoordinate()
	coordhyper.SetCoordinateSystemToNormalizedViewport()
	coordhyper.SetValue(0.1,0.05)
	scalarBarhyper.SetWidth(.8)
	scalarBarhyper.SetHeight(.15)
	hyperactor = vtk.vtkActor()
	hyperactor.SetMapper(mrihypermapper)
	rendererhyper = vtk.vtkRenderer()
	rendererhyper.AddActor(hyperactor)
	rendererhyper.AddActor(scalarBarhyper)
	rendererhyper.SetViewport(xmins[1],ymins[1],xmaxs[1],ymaxs[1])
	return rendererhyper





renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(1024, 768) # Set the window size you want
renderWindow.AddRenderer(mapmrihyper())
renderWindow.AddRenderer(mapmri())

# Set-up interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()

# Use track-ball interaction style instead of joystick style
style = vtk.vtkInteractorStyleTrackballCamera()

renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()

