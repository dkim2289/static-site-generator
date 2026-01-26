import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    # if the destination dir doesn't exsits
    if not os.path.exists(dest_dir_path):
        # it creates one.
        os.mkdir(dest_dir_path)
    # for every file in the source dir
    for filename in os.listdir(source_dir_path):
        # getting a full file path (combine source dir and filename)
        from_path = os.path.join(source_dir_path, filename)
        # does the same for the dest path (combime dest dir and filename)
        dest_path = os.path.join(dest_dir_path, filename)
        # logs (to spot bugs)
        print(f" * {from_path} -> {dest_path}")
        # if from_path is confirmed to be a file,
        if os.path.isfile(from_path):
            # copy the file (from the source dir to the dest dir)
            shutil.copy(from_path,dest_path)
        # if confirmed not a file
        else:
            # that means it's a directory. So, use the whole function recursively. to copy the whole filetree
            copy_files_recursive(from_path, dest_path)