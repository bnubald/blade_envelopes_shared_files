import bpy, bmesh
import numpy as np
import os, sys, glob
from math import radians
from mathutils import Vector

## Start of code
# Get this script location
filepath = bpy.context.space_data.text.filepath

# Move to script path
abspath = bpy.path.abspath(filepath)
dname = os.path.dirname(abspath)

os.chdir(dname)

# Add script path to module import list
sys.path.insert(0, os.getcwd())

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def create_curve(coords, curvename):
    curve = bpy.data.curves.new('crv', 'CURVE')
    curve.dimensions = '3D'
    spline = curve.splines.new(type='NURBS')
    spline.points.add(len(coords) - 1) 
    
    # (add nurbs weight to coordinates)
    coords = np.column_stack( (coords, np.ones(len(coords))) )
    for p, new_co in zip(spline.points, coords):
        p.co = new_co
    spline.use_endpoint_u = True
    spline.use_endpoint_v = True
    obj = bpy.data.objects.new(curvename, curve)
    obj.data.resolution_u     = 1             # Preview U
    obj.data.fill_mode        = 'FULL'        # Fill Mode ==> Ful
    bpy.data.scenes[0].collection.objects.link(obj)


# Main code
print( os.getcwd() )

baseline_csv = "baseline-frompyscript.csv"
verts = np.loadtxt(baseline_csv, delimiter=',', skiprows=1)

# Now that we know the vertex locations, delete imported ply object
bpy.ops.object.delete()

curvename = "baseline-frompyscript"
create_curve( verts, curvename )
obj = bpy.data.objects[curvename]

print("Context mode:", bpy.context.mode)

obj.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[curvename]
bpy.ops.object.convert(target='MESH', keep_original=False)