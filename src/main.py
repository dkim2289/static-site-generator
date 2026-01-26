import os
import shutil

from copystatic import copy_files_recursive

# static dir filepath
dir_path_static = "./static"
# public dir filepath
dir_path_public = "./public"

def main():
    # printing a msg indicating clearing the public dir. so copies can be made successfully 
    print("Deleting public directory...")
    # if the target path, or destination path, or target path, already exist,
    if os.path.exists(dir_path_public):
        # it deletes the whole tree
        shutil.rmtree(dir_path_public)
    # print a msg that copying now starts 
    print("Copying static files to public directories...")
    # copy the whole filetree
    copy_files_recursive(dir_path_static,dir_path_public)



if __name__ == "__main__":
    main()
