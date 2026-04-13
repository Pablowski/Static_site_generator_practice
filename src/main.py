from textnode import *
from block_markdown import *
from generate_page import *
from copystatic import copy_directory

def main():
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()