import sys
import vtk

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "[filename]")
    exit()

#filename = sys.argv[1]

# Create a renderer
renderer = vtk.vtkRenderer()

# Read the file

#generic_reader = vtk.vtkDataSetReader()
#generic_reader.SetFileName(filename)
#generic_reader.Update()

topographymapper = vtk.vtkDataSetMapper()
topographymapper = vtk.vtkDataSetMapper()
delaunaymapper = vtk.vtkPolyDataMapper()  #i.e., vtkDataSet and all derived classes
interploationmapper = vtk.vtkPolyDataMapper()
topographyactor = vtk.vtkActor()
delaunayactor = vtk.vtkActor()
interpolationactor = vtk.vtkActor() # geometry & properties

def delaunay():

    triangulation_filter = vtk.vtkDelaunay2D()
    triangulation_filter.SetInputConnection(generic_reader.GetOutputPort())
    triangulation_filter.Update()
    return triangulation_filter

def warpdelaunay(tfilt):
    wd = vtk.vtkWarpScalar()
    wd.SetInputConnection(tfilt.GetOutputPort())
    wd.SetScaleFactor(2)
    delaunaymapper.SetInputConnection(wd.GetOutputPort())
    delaunayactor.SetMapper(delaunaymapper)
    delaunayactor.GetProperty().SetRepresentationToWireframe()
    #delaunayactor.GetProperty().SetEdgeColor(0, 0, 1)
    delaunayactor.GetProperty().SetInterpolationToFlat()


# create mapper

mapper = vtk.vtkDataSetMapper()
mapper2 = vtk.vtkPolyDataMapper()
def readfiles(generic_reader):
    if generic_reader.GetPolyDataOutput():
        print( "Reading polydata")
        polydata = generic_reader.GetPolyDataOutput()
        pdata = polydata
        triangulation = delaunay()
        warpdelaunay(triangulation)
        # triangulation code here...
    
        # mapper.SetInputConnection(triangulation_filter.GetOutputPort()) 

        # set the appropriate scalar range for color mapping

        delaunaymapper.SetScalarRange(polydata.GetPointData().GetArray(0).GetRange())
        a,b = polydata.GetPointData().GetArray(0).GetRange()
        lut = vtk.vtkColorTransferFunction()
        h = 0
        s = 0
        v = 0
        step = 100
        inc = (1/(b/step))
        vinc = (59/(b/step))
        for i in range(int(a), int(b), step):
            lut.AddHSVPoint(i, 30, s, 59)
            s += inc
            v += vinc
        delaunaymapper.SetLookupTable(lut)
    elif generic_reader.GetStructuredPointsOutput():
        print("Reading Structured points")

        pdata = vtk.vtkDataSetReader()
        pdata.SetFileName(sys.argv[1])
        pdata.Update() 

        geom = vtk.vtkImageDataGeometryFilter()
        geom.SetInputConnection(generic_reader.GetOutputPort())

        warp = vtk.vtkWarpScalar()
        warp.SetInputConnection(geom.GetOutputPort())
        warp.SetNormal(0, 0, 1)
        warp.UseNormalOn()
        warp.SetScaleFactor(1)
        warp.Update()

        center = warp.GetOutput().GetCenter()

        sphere = vtk.vtkSphere()
        sphere.SetCenter(center[0],center[1]-7500,center[2])
        
        attr = vtk.vtkSampleImplicitFunctionFilter()
        attr.SetInputData(pdata.GetOutput())
        attr.SetImplicitFunction(sphere)
        attr.Update()

        shep = vtk.vtkShepardKernel()
        shep.SetPowerParameter(2)
        shep.SetRadius(10)
        interpolator = vtk.vtkPointInterpolator2D()
        interpolator.SetInputConnection(warp.GetOutputPort()) # cloud
        interpolator.SetSourceConnection(attr.GetOutputPort()) # image
        interpolator.SetKernel(shep)
        interpolator.GetLocator().SetNumberOfPointsPerBucket(1)

        # set the appropriate scalar range for color mapping
        #mapper2.SetScalarRange(interpolator.GetStructuredPointsOutput().GetPointData().GetArray(0).GetRange())
    
        mapper2.SetInputConnection(interpolator.GetOutputPort())
        
    elif generic_reader.GetUnstructuredGridOutput():
        print("Reading Unstructured grid")
    
        # set the appropriate scalar range for color mapping
        mapper.SetScalarRange(generic_reader.GetUnstructuredGridOutput().GetPointData().GetArray(0).GetRange())
    
        mapper.SetInputConnection(generic_reader.GetOutputPort())
    
    else:
        print("No reader written for this file type!")

i = 1
while i < 3:
    filename = sys.argv[i]
    # Read the file
    generic_reader = vtk.vtkDataSetReader()
    generic_reader.SetFileName(filename)
    generic_reader.Update()
    readfiles(generic_reader)
    i+=1



# create actor
actor = vtk.vtkActor()
actor.SetMapper(mapper2)


# Create a renderer and add the actor to the scene
renderert = vtk.vtkRenderer()
rendereri = vtk.vtkRenderer()
rendereri.AddActor(actor)
renderert.AddActor(delaunayactor)



xmins=[0,0]
xmaxs=[1,1]
ymins=[0,0.5]
ymaxs=[0.5,1]

rendereri.SetViewport(xmins[0],ymins[0],xmaxs[0],ymaxs[0])
renderert.SetViewport(xmins[1],ymins[1],xmaxs[1],ymaxs[1])

# Create render window 
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(1024, 768) # Set the window size you want
renderWindow.AddRenderer(renderert)
renderWindow.AddRenderer(rendereri)

# Set-up interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()

# Use track-ball interaction style instead of joystick style
style = vtk.vtkInteractorStyleTrackballCamera()

renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()

