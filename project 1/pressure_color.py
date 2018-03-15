import sys
import vtk

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "[filename]")
    exit()

renderer = vtk.vtkRenderer()

filename = sys.argv[1]

generic_reader = vtk.vtkDataSetReader()
generic_reader.SetFileName(sys.argv[1])
generic_reader.Update()

tmap = vtk.vtkDataSetMapper()


#structured

a,b = generic_reader.GetUnstructuredGridOutput().GetPointData().GetArray(0).GetRange()
tcol = vtk.vtkColorTransferFunction()
tcol.AddHSVPoint(a, 0, 0, 0)
tcol.AddHSVPoint(b/4, 0, 0.5, 0.5)
tcol.AddHSVPoint(b*3/4, 0, 0.75, 0.75)
tcol.AddHSVPoint(b*7/8, 0, 0.875, 0.875)
tcol.AddHSVPoint(b, 0, 1, 1)



points = generic_reader.GetUnstructuredGridOutput().GetPointData().GetArray(0)
generic_reader.GetUnstructuredGridOutput().GetPointData().SetScalars(points)
tmap.SetInputConnection(generic_reader.GetOutputPort())
tmap.SetLookupTable(tcol)
tmap.SetScalarRange(a,b)


scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(tmap.GetLookupTable() )
scalarBar.SetOrientationToHorizontal()
scalarBar.GetLabelTextProperty().SetColor(1,1,1)


# position it in window
coord = scalarBar.GetPositionCoordinate()
coord.SetCoordinateSystemToNormalizedViewport()
coord.SetValue(0.1,0.05)
scalarBar.SetWidth(.8)
scalarBar.SetHeight(.15)

# Create a renderer
renderer = vtk.vtkRenderer()

# create actor
actor = vtk.vtkActor()
actor.SetMapper(tmap)


# Create a renderer and add the actor to the scene
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(scalarBar)

#renderer.AddActor(delaunayactor)

# Create render window 
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(1024, 768) # Set the window size you want
renderWindow.AddRenderer(renderer)

# Set-up interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()

# Use track-ball interaction style instead of joystick style
style = vtk.vtkInteractorStyleTrackballCamera()

renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()

