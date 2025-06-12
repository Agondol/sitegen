from file_ops import (
    copy_contents,
    generate_pages_recursive,
)

from textnode import (
    TextNode,
    TextType,
)

SOURCE_DIRECTORY = r"/home/agondol/Documents/Courses/BootDev/sitegen/static"
DESTINATION_DIRECTORY = r"/home/agondol/Documents/Courses/BootDev/sitegen/public"

def main():
    copy_contents(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()