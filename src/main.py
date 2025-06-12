from file_ops import (
    copy_contents,
)

from textnode import (
    TextNode,
    TextType,
)

SOURCE_DIRECTORY = r"/home/agondol/Documents/Courses/BootDev/sitegen/static"
DESTINATION_DIRECTORY = r"/home/agondol/Documents/Courses/BootDev/sitegen/public"

def main():
    copy_contents(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)
    node = TextNode("Boot.Dev is cool!", TextType.LINK, "https://boot.dev")
    print(node)

if __name__ == "__main__":
    main()