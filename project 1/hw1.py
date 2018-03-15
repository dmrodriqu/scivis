import sys
import vtk


if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "[filename]")
    exit()

filename = sys.argv[1]

generic_reader = vtk.vtkDataSetReader()
generic_reader.SetFileName(sys.argv[1])
generic_reader.Update()


topread = vtk.vtkDataSetReader()
topread.SetFileName(sys.argv[2])
topread.Update()

topographymapper = vtk.vtkDataSetMapper()
topographymapper = vtk.vtkDataSetMapper()
delaunaymapper = vtk.vtkPolyDataMapper()  #i.e., vtkDataSet and all derived classes
interploationmapper = vtk.vtkPolyDataMapper()
topographyactor = vtk.vtkActor()
delaunayactor = vtk.vtkActor()
interpolationactor = vtk.vtkActor() # geometry & properties
# Create a renderer
renderer = vtk.vtkRenderer()


def delaunay():
    # triangulation and interpolation
    #create class
    triangulation_filter = vtk.vtkDelaunay2D()
    # get input data from point cloud
    triangulation_filter.SetInputConnection(generic_reader.GetOutputPort())
    triangulation_filter.Update()
    return triangulation_filter
    # map mesh
#    delaunaymapper.SetInputConnection(triangulation_filter.GetOutputPort())
#    delaunayactor.SetMapper(delaunaymapper)
#    delaunayactor.GetProperty().SetRepresentationToWireframe()
#    delaunayactor.GetProperty().SetEdgeColor(0, 0, 1)
#    delaunayactor.GetProperty().SetInterpolationToFlat()


# Create a renderer and add the actor to the scene

def warpdelaunay():
    triangulation_filter =  delaunay()
    wd = vtk.vtkWarpScalar()
    wd.SetInputConnection(triangulation_filter.GetOutputPort())
    wd.SetScaleFactor(1)
    delaunaymapper.SetInputConnection(wd.GetOutputPort())
    delaunayactor.SetMapper(delaunaymapper)
    delaunayactor.GetProperty().SetRepresentationToWireframe()
    delaunayactor.GetProperty().SetEdgeColor(0, 0, 1)
    delaunayactor.GetProperty().SetInterpolationToFlat()

def interpolate():
    geom = vtk.vtkImageDataGeometryFilter()
    geom.SetInputConnection(topread.GetOutputPort())
    warp2 = vtk.vtkWarpScalar()
    warp2.SetInputConnection(geom.GetOutputPort())
    warp2.SetNormal(0, 0, 1)
    warp2.UseNormalOn()
    warp2.SetScaleFactor(2)
    warp2.Update()
    sphere = vtk.vtkSphere()
    center = warp2.GetOutput().GetCenter()
    sphere.SetCenter(center[0], center[1]-7500, center[2])
    attr = vtk.vtkSampleImplicitFunctionFilter()
    attr.SetInputData(topread.GetOutput())
    attr.SetImplicitFunction(sphere)
    attr.Update()
    shep = vtk.vtkShepardKernel()
    shep.SetPowerParameter(2)
    shep.SetRadius(1)
    interpolator = vtk.vtkPointInterpolator2D()
    interpolator.SetInputConnection(warp2.GetOutputPort())
    interpolator.SetSourceConnection(attr.GetOutputPort())
    interpolator.SetKernel(shep)
    interpolator.SetNullPointsStrategyToClosestPoint()
    interploationmapper.SetInputConnection(interpolator.GetOutputPort())
    interpolationactor.SetMapper(interploationmapper)


warpdelaunay()
interpolate()
renderer = vtk.vtkRenderer()
#renderer.AddActor(delaunayactor)
renderer.AddActor(interpolationactor)
renderer.AddActor(delaunayactor)

# Create render window
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(900, 600) # Set the window size you want
renderWindow.AddRenderer(renderer)

# Set-up interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()

# Use track-ball interaction style instead of joystick style
style =	vtk.vtkInteractorStyleTrackballCamera()

renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()
