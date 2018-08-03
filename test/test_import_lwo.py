import bpy

# import sys
# sys.path.append("E:\\blender-addons\\test\\test_helper.py")
from test_helper import setup, cleanup, copy_plugin, diff_files

def main(infile, module):
    copy_plugin("../io_import_scene_lwo.py")
    
    outfile0, outfile1 = setup(infile, module)

    bpy.ops.import_scene.lwo(filepath=infile)
    bpy.ops.wm.save_mainfile(filepath=outfile0)

    cleanup(module)
    
    diff_files(outfile0, outfile1)
    

if __name__ == '__main__':
    #infile = 'src_lwo/Phobos/objects/USS-Phobos.lwo'
    #infile = 'src_lwo/Phobos/objects/USS-Phobos_reg.11.5.lwo'
    #infile = 'src_lwo/box/box0.lwo'
    infile = 'src_lwo/box/box1.lwo'
    module = 'io_import_scene_lwo'
    main(infile, module)
