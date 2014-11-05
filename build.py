"""build.py
Runs xacro on the files listed in the 'definitions' directory and builds the models

Usage:
  build.py [--only=NAMES] [--symlink=MODEL_SYM_PATH] [--xacro=XACRO_CONVERTER]

Options:
  -h --help     Show this screen.
  --only=NAMES        Creates only the models listed (separated by comma)
  --symlink=MODEL_SYM_PATH     When finished, creates a symlink at MODEL_SYM_PATH that points to the directories in the 'model' directory. 
  --xacro=XACRO_CONVERTER       Use the specified xacro converter

"""
import os

try:
    from docopt import docopt
    from plumbum import local
    import logging
    import coloredlogs
except ImportError, err:
    module_name = err.args[0].split()[-1]
    print("Some of the needed modules were missing (at least `%s')." % module_name)
    print("Please check that all dependencies are correctly installed.")
    print("To do so, it is suggested to use the command:")
    print("     $ sudo pip install docopt plumbum logging colored logs")
    exit()


import shutil
import re
logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO)

def assure_dir_exist(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def null_or_empty(s):
    return s == None or s == ""

def clean_xacro_output(f):
    lines = []
    with open(f, 'r') as sdf:
        lines = sdf.readlines()
        lines[5] = lines[5].replace(' xmlns:xacro="http://www.ros.org/wiki/xacro"', '')
    os.remove(f)
    with open(f, 'w') as sdf:
        sdf.writelines(lines)

def clean_output_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

class Build():
    def __init__(self, opt):
        self.opt = opt
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.defs_dir = script_dir+'/definitions'
        self.models_dir = script_dir+'/models'
        # TODO: call directly xacro lib in python?
        xacro_converter_exe = opt['--xacro'] 
        if null_or_empty(xacro_converter_exe):
            self.xacro_converter = local["rosrun"]["xacro", "xacro"]
        else:
            splitted = re.compile("[ ]+").split(xacro_converter_exe)
            self.xacro_converter = local[splitted[0]][splitted[1:]]
        only = opt['--only']
        self.avaiable_defs = os.listdir(self.defs_dir)
        self.linkdir = opt['--symlink']
        if null_or_empty(only):
            self.defs = self.avaiable_defs
        else:
            self.defs=only.split(',')

    def start(self):
        fails=[]
        success=[]
        for name in self.defs:
            print("Building {}".format(name))
            indir=self.defs_dir + "/" + name
            outdir=self.models_dir + "/" + name
            infile=indir + "/model.xacro"
            outfile=outdir + "/model.sdf"
            assure_dir_exist(outdir)
            try:
                (self.xacro_converter[infile] > outfile)()
                clean_xacro_output(outfile)
                success.append(name)
            except Exception as e:
                fails.append((name, e))
            shutil.copyfile(indir+"/model.config", outdir+"/model.config")
            dirs_to_copy_names = ["/meshes", "/textures"]
            for dir_name in dirs_to_copy_names:
                mesh_dir_name = indir + dir_name
                out_mesh_dir = outdir + dir_name
                if os.path.exists(mesh_dir_name):
                    clean_output_dir(out_mesh_dir)
                    shutil.copytree(mesh_dir_name, out_mesh_dir)
        if len(fails) > 0:
            logger.error("{} models failed:\n".format( str(len(fails))) )
            for fail in fails:
                logger.error("while building {}:\n {}".format(fail[0], str(fail[1])))
        print("{}/{} available models created".format(
            str(len(success)), 
            str(len(self.avaiable_defs))
            )) 
        if not null_or_empty(self.linkdir):
            self.link(success, self.linkdir)

    def link(self, names, linkdir):
        for name in names: 
            source=self.models_dir + "/" + name
            linkname=os.path.expanduser(linkdir) + "/" + name
            errors=[]
            if os.path.lexists(linkname):
                errors.append((name, linkname))
            else:
                local['ln']['-s', source, linkname]()
            if len(errors) > 0:
                error_list = [ "{} at {}".format(n, e) for (n, e) in errors]
                error_list = "\n".join(error_list)
                logger.warning("Could not create links for these models: " + 
                        "{}\nDirectories already existed".format(error_list))
        print("done linking")


if __name__ == '__main__':
    arguments = docopt(__doc__)
    build = Build(arguments)
    build.start()

