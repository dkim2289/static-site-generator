import os
import shutil
import sys

from copystatic import copy_files_recursive
from markdown_blocks import (
    # generate_page,
    generate_pages_recursive,
)

# use the sys.argv to grab the first CLI argument to the program.
# Save it as the basepath. If one isn't provided, default to "/".
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"


# static dir filepath
dir_path_static = "./static"
# public dir filepath
dir_path_public = "./docs"



def main():
    # printing a msg indicating clearing the public dir. so copies can be made successfully
    print("Deleting public directory...")
    # if the target path, or destination path, already exist,
    if os.path.exists(dir_path_public):
        # it deletes the whole tree, just in case the copying doesn't work properly because of it
        shutil.rmtree(dir_path_public)
    # print a msg that copying now starts
    print("Copying static files to public directories...")
    # copy the whole filetree
    copy_files_recursive(dir_path_static,dir_path_public)

    # using "generate_pages_recursive" instead of "generate_page"
    # updating to build the site into the docs directory instaed of public.
    generate_pages_recursive("content", "template.html", "docs", basepath)

    # # generate a page from "content/index.md" using "template.html" and write it to "public/index.html"
    # generate_page("content/index.md", "template.html", "public/index.html")

    # # generate "content/blog/glorfindel/index.md"
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")

    # # generate "content/blog/tom/index.md"
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")

    # # generate "content/blog/majesty/index.md"
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")

    # # generate "contact/index.md"
    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")



if __name__ == "__main__":
    main()
