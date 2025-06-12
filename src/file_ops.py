import os
import shutil
import re

from markdown import (
    markdown_to_html_node,
    extract_title,
)

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)

def copy_contents(source, destination):
    if os.path.exists(destination):
        dir_contents = os.listdir(destination)
        if len(dir_contents):
            for i in dir_contents:
                destination_item = f"{destination}/{i}"
                if os.path.isdir(destination_item):
                    print(f"Removing directory {destination_item}.")
                    shutil.rmtree(destination_item)
                else:
                    print(f"Removing file {destination_item}.")
                    os.remove(destination_item)
                    
        if os.path.exists(source):
            dir_contents = os.listdir(source)
            if len(dir_contents):
                for i in dir_contents:
                    source_item = f"{source}/{i}"
                    destination_item = f"{destination}/{i}"
                    if os.path.isfile(source_item):
                        print(f"Copying file {source_item} to {destination_item}")
                        shutil.copy(source_item, destination_item)
                    else:                        
                        print(f"Creating directory {destination_item}.")
                        os.mkdir(destination_item)
                        copy_contents(source_item, destination_item)
        else:
            raise FileNotFoundError("The source directory does not exist!")
    else:
        raise FileNotFoundError("The destination directory does not exist!")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path):
        with open(from_path, "r") as f:
            from_contents = f.read()
    else:
        raise FileNotFoundError(f"From_path file not found {from_path}")
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            template_contents = f.read()
    else:
        raise FileNotFoundError(f"Template_path file not found {template_path}")
    node = markdown_to_html_node(from_contents)
    html = node.to_html()
    title = extract_title(from_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    if not os.path.exists(dest_path):
        split_path = dest_path.split('/')[0:-1]
        current_path = ""
        for p in split_path:
            if p == ".":
                current_path += "."
                continue
            current_path += f"/{p}"            
            if not os.path.exists(current_path):
                os.mkdir(current_path)
    with open(dest_path, "w") as f:
        f.writelines(template_contents)
    print("Finished generating page.")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"The content path directory does not exists.")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"The template path does not exists.")
    
    folder_items = os.listdir(dir_path_content)
    for i in folder_items:
        item_path = f"{dir_path_content}/{i}"
        dest_path = f"{dest_dir_path}/{i}"
        if os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dest_path)
        else:
            matches = re.search(r".*(\.md)$", item_path)
            if matches:
                generate_page(item_path, template_path, dest_path.replace(matches[1], ".html"))
        