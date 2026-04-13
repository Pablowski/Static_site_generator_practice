import os
import shutil

def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst,item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied {src_path} to {dst_path}")
        else:
            copy_directory(src_path, dst_path)
