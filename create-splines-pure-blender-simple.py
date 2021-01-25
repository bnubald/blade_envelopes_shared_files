import bpy, bmesh
import numpy as np
import os, sys, glob
from math import radians
from mathutils import Vector

## User-inputs
tube_radius = 0.0001
nsamples = 40

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

def create_tube(coords, curvename):
    """
    Creates a 3D tube geometry.
    
    Parameters
    ----------
    coords: numpy array
        3D coordinate profile
    curvename: string
        Name of the output mesh object
    """
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
    obj.data.fill_mode        = 'FULL'        # Fill Mode ==> Full
    obj.data.bevel_depth      = tube_radius   # Bevel Depth
    obj.data.bevel_resolution = 10            # Bevel Resolution

    bpy.data.scenes[0].collection.objects.link(obj)
    
    return

def set_material(obj, name, rgba):
    """
    Creates a new material using rgb values.
    Overwrites any existing material with same name.
    
    Parameters
    ----------
    obj: blender object
        Object to which the material property should be assigned to
    name: string
        Name of the new material
    rgba: list
        Name of the new material
    """
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    else:
        bpy.data.materials.remove(material)
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes

    principled_bsdf = nodes['Principled BSDF']
    if principled_bsdf is not None:
        principled_bsdf.inputs[0].default_value = rgba
        principled_bsdf.inputs['Roughness'].default_value = 0.0
        principled_bsdf.inputs['Transmission'].default_value = 0.8
    material.shadow_method = 'NONE'
    obj.active_material = material

    return

#Re-obtaining PRGn values
def PRGn(cmap, values):
    x = values
    xp = np.linspace(0, 1, num=len(cmap))
    rgba = np.zeros( (len(values), cmap.shape[1]) )
    for i in range(0, cmap.shape[1]):
        fp = cmap[:, i]
        rgba[:, i] = np.interp( x, xp, fp )

    return rgba


# Main code
np.random.seed(0)

lossdata = np.load( "blade_envelopes.npz" )
x_coords = lossdata['x']
y_coords_nzm = lossdata['y']

plot_x = x_coords[0]
y_coords = y_coords_nzm - np.tile(np.mean(y_coords_nzm, axis=1).reshape(1,-1).T, (1,240)) + np.mean(y_coords_nzm)

LE_SS = range(200,220)
LE_PS = range(225,240)
PS_range = list(range(220, 240)) + list(range(90))
SS_range = range(90, 220)

LE_SS_disp = []
LE_PS_disp = []

for i in range(y_coords.shape[0]):
    LE_SS_disp.append(np.mean((y_coords[i] - np.mean(y_coords, axis=0))[LE_SS]))
    LE_PS_disp.append(np.mean((y_coords[i] - np.mean(y_coords, axis=0))[LE_PS]))

# Normalize color data
norm1 = NormalizeData(LE_SS_disp)
norm2 = NormalizeData(LE_PS_disp)

# Read colormap generated using python with matplotlib (store-matplotlib-colourmap-for-blender.py)
data = np.load('PRGn-colourmap.npz')
cmap = data['cmap']

# Get RGBA colour values for matplotlib PRGn colourmap
rgba_ss = PRGn(cmap, norm1)
rgba_ps = PRGn(cmap, norm2)

for i in range(nsamples):
    cid = i + 1

    ##Suction surf points
    this_plot_y = np.hstack([y_coords_nzm[i], y_coords_nzm[i][0]])
    Xcoords = plot_x[SS_range]
    Ycoords = this_plot_y[SS_range]
    ss_points = np.column_stack( (Xcoords, Ycoords, np.zeros(Xcoords.shape)) )

    #Create 3D curves
    curvename = "tube_ss_" + str(cid)
    create_tube( ss_points, curvename )
    obj = bpy.data.objects[curvename]
    set_material( obj, "tube_ss_" + str(cid), rgba_ss[i] )


    ##Pressure surf points
    Xcoords = np.hstack([plot_x[SS_range][-1], plot_x[PS_range], plot_x[SS_range][0] ])
    Ycoords = np.hstack([this_plot_y[SS_range][-1], this_plot_y[PS_range], this_plot_y[SS_range][0] ])
    ps_points = np.column_stack( (Xcoords, Ycoords, np.zeros(Xcoords.shape)) )

    curvename = "tube_ps_" + str(cid)
    create_tube( ps_points, curvename )
    obj = bpy.data.objects[curvename]
    set_material( obj, "tube_ps_" + str(cid), rgba_ps[i] )