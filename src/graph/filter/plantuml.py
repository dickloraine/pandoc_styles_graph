#!/usr/bin/env python3

"""
Converts a codeblock containing plantuml code to an image and links that image.

The name of the produced file is generated from the hash of the code.

The image gets a class of 'plantuml' to make special styling possible.

You can give the image a caption with the attribute 'caption'.

The image is saved in the current folder by default. To change this, either set the
attribute 'folder' in the codeblock or globaly in the metadata block with the field
'plantuml-image-folder'.

If the plantuml cl-command is not just 'plantuml' for your system, you can set the
command with the metadata field 'plantuml-path'
"""
import hashlib
import os
from pandoc_styles import run_pandoc_styles_filter, CodeBlock, run_process, file_write


def plantuml(self):
    width = f'width={self.attributes.get("width")}' if self.attributes.get("width") else ""
    height = f'height={self.attributes.get("height")}' if self.attributes.get("height") else ""
    file_name_hash = hashlib.md5(self.text.encode('utf-8')).hexdigest()[:9]
    file_name = f"{file_name_hash}.png"
    folder = self.attributes.get("folder") or self.get_metadata("plantuml-image-folder")
    caption = self.attributes.get("caption", "")
    if folder:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, file_name)

    if not os.path.isfile(file_name):
        cmd = self.get_metadata("plantuml-path", "plantuml")
        temp_file = file_write(f"{file_name_hash}.plt",
                               f"@startuml\n{self.text}\n@enduml")
        if folder:
            run_process(f'{cmd} {temp_file} -o "{os.path.normpath(folder)}"', True)
        else:
            run_process(f'{cmd} {temp_file}', True)
        os.remove(temp_file)
    return f"![{caption}]({file_name}){{.plantuml {width} {height}}}"


if __name__ == "__main__":
    run_pandoc_styles_filter(plantuml, CodeBlock, ["plantuml", "puml"])
