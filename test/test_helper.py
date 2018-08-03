import bpy
import os
import sys
import re
import zipfile

def setup(infile):
    print("Setting up!")
    name = os.path.basename(infile)
    outfile0 = 'dst_blend/{0}.blend'.format(name)
    outfile1 = 'ref_blend/{0}.blend'.format(name)
#     for x in bpy.data.objects.keys():
#         print(x)
#         bpy.data.objects[x].select = True
#         bpy.ops.object.delete()
    if 'Camera' in bpy.data.objects.keys():
        bpy.data.objects['Camera'].select = True
        bpy.ops.object.delete()
    if 'Lamp' in bpy.data.objects.keys():
        bpy.data.objects['Lamp'].select = True
        bpy.ops.object.delete()
    if 'Cube' in bpy.data.objects.keys():
        bpy.data.objects['Cube'].select = True
        bpy.ops.object.delete()

    if os.path.isfile(outfile0):
        os.unlink(outfile0)
    
    directory = "ref_blend"
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = "dst_blend"
    if not os.path.exists(directory):
        os.makedirs(directory)


    return(outfile0, outfile1)

def cleanup(module):
    print("Cleaning up!")
    bpy.ops.wm.addon_disable(module=module)
#     directory = "dst_blend"
#     if not os.path.exists(directory):
#         os.makedirs(directory)




def copy_plugin(infile, expect_version=(-1, -1, -1)):
    print("Copying plugin!")
    
    infile = os.path.realpath(infile)
    module = re.sub(".py", "", os.path.basename(infile))
    zfile =  os.path.realpath(module + ".zip")
    
    zf = zipfile.ZipFile(zfile, "w")
    if os.path.isdir(infile):
        for dirname, subdirs, files in os.walk(infile):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
    else:
        zf.write(infile)
    zf.close()
    
    bpy.ops.wm.addon_install(overwrite=True, filepath=zfile)

    bpy.ops.wm.addon_enable(module=module)

    #print(bpy.context.user_preferences.addons.keys())
        
    mod = sys.modules[module]
    return_version = mod.bl_info.get('version', (-1, -1, -1))
    if not expect_version == return_version:
        print("ERROR, versions do not match:")
        print("\tnot {0} == {1}".format(expect_version, return_version))


    return module

 
#     user = os.environ['USER']
#     files = glob("C:\\Users\\{0}\\AppData\\Roaming\\Blender Foundation\\Blender\\*\\scripts\\addons".format(user))
#     #print(files)
#     if 1 == len(files):
#         dst0 = files[0]
#     elif 0 == len(files):
#         print("Cannot find addons directory for user: {0}".format(user))
#     else:
#         raise
#     
#     if os.path.isfile(infile):
#         name = os.path.basename(infile)
#         #print(name)
#         src = infile
#         
#         dst = "{0}\\{1}".format(dst0, name)
#         if os.path.isfile(dst):
#             os.unlink(dst)
#     
#         #print(src)
#         #print(dst)
#         copyfile(src, dst)
#     #else:
#     #copy_tree(src, dst)

def compare_obj(x, y):
    #from mathutils import Vector, Matrix, Euler, Quaternion
    fail = False
    
    if str(x).startswith("<bpy_boolean") or \
       str(x).startswith("<bpy_int") or \
       str(x).startswith("<bpy_float") or \
       str(x).startswith("<bpy_collection"):
        if not len(x) == len(y):
            fail = True
        else:
            for i in range(len(x)):
                fail = compare_obj(x[i], y[i])
    elif str(x).startswith("<bpy_func"):
        #print(x1, True)
        return None
    elif str(x).startswith("<bpy_struct"):
        #print(a, x1)
        return None
#     elif x is None or \
#        isinstance(x, str) or \
#        isinstance(x, int) or \
#        isinstance(x, float) or \
#        isinstance(x, list) or \
#        isinstance(x, tuple) or \
#        isinstance(x, Quaternion) or \
#        isinstance(x, Euler) or \
#        isinstance(x, Matrix) or \
#        isinstance(x, Vector):
#         if not x == y:    
#             fail = True
    else:
        if not x == y:    
            fail = True
        #fail = True
       
    return fail

def compare_bpy(a, x, y, error_count = 0):
    from mathutils import Vector, Matrix, Euler, Quaternion
    fail = False
    try:
        x1 = getattr(x,a)
    except:
        print("ERROR: x1 does not have attribute: {0}".format(a))
    try:
        y1 = getattr(y,a)
    except:
        print("ERROR: y1 does not have attribute: {0}".format(a))
    
    if 'active_material' == a or \
       'material_slots' == a:
        #print(x1, True)
        pass
    else:
        fail = compare_obj(x1, y1)
        #print(a, fail, x1)
    
    if fail:
        error_count += 1
        print("ERROR: Attributes do not match: {0} - {1} - {2}".format(a, x1, y1))
    
    return error_count

def diff_files(outfile0, outfile1, error_count=0):
    print("Diffing files!")
    if os.path.isfile(outfile1):
        print("Reference blend present: {0}".format(outfile1))
    else:
        print("No reference blend present: {0}".format(outfile1))
        exit()
    
    bpy.ops.wm.open_mainfile(filepath=outfile0)
    o0 = {}
    for k in bpy.data.objects.keys():
        o0[k] = bpy.data.objects[k].copy()
    
    bpy.ops.wm.open_mainfile(filepath=outfile1)
    o1 = {}
    for k in bpy.data.objects.keys():
        o1[k] = bpy.data.objects[k].copy()

    if not len(o0.keys()) == len(o1.keys()):
        error_count += 1
        print("ERROR: Incorrect number of objects generated", error_count)
        #raise

    for k in o0.keys():
        x = o0[k]
        y = o1[k]
        #pprint(dir(x))
        attr_list = dir(x)
        attr_list.remove('MeasureGenerator')
        attr_list.remove('__doc__')
        attr_list.remove('__module__')
        attr_list.remove('__slots__')
        for a in attr_list:
            error_count = compare_bpy(a, x, y, error_count)
        print("Test completed with {0} errors".format(error_count))
        
