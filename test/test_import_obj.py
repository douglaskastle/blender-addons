import bpy

# import sys
# sys.path.append("E:\\blender-addons\\test\\test_helper.py")
from test_helper import setup, cleanup, copy_plugin, diff_files

def main(infile, plugin, expect_version):
    module = copy_plugin(plugin, expect_version)
    
    outfile0, outfile1 = setup(infile)

    bpy.ops.import_scene.obj(filepath=infile)
    bpy.ops.wm.save_mainfile(filepath=outfile0)

    cleanup(module)
    
    diff_files(outfile1, outfile0)
    

if __name__ == '__main__':
    #infile = 'src_lwo/Phobos/objects/USS-Phobos.lwo'
    #infile = 'src_lwo/Phobos/objects/USS-Phobos_reg.11.5.lwo'
    #infile = 'src_lwo/box/box0.lwo'
    infile = 'src_lwo/box/box1.obj'
    #module = 'io_scene_obj'
    plugin = "../io_scene_obj"
    expect_version = (2, 3, 6)
    
    main(infile, plugin, expect_version)
