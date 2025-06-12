import os
import shutil

def copy_contents(source, destination):
    if os.path.exists(destination):
        dir_contents = os.listdir(destination)
        if len(dir_contents):
            for i in dir_contents:
                if os.path.isdir(i):
                    shutil.rmtree(i)
                else:
                    os.remove(i)
        if os.path.exists(source):
            dir_contents = os.listdir(source)
            if len(dir_contents):
                for i in dir_contents:
                    if os.path.isfile(i):
                        shutil.copy(source, destination)
                    else:
                        source_dir = f"{source}/{i}"
                        destination_dir = f"{destination}/{i}"
                        os.mkdir(destination_dir)
                        copy_contents(source_dir, destination_dir)
        else:
            raise FileNotFoundError("The source directory does not exist!")
    else:
        raise FileNotFoundError("The destination directory does not exist!")