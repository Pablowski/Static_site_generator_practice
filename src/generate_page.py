import os
from block_markdown import * 

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('srv="/', f'src="{basepath}')


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(content_dir, template_path, dest_dir, basepath="/"):
    for item in os.listdir(content_dir):
        src_path = os.path.join(content_dir,item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(src_path, template_path, dest_path, basepath)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
        