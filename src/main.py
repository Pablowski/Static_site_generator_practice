import sys
from generate_page import *
from copystatic import copy_directory

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()