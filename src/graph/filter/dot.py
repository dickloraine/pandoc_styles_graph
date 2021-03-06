"""
Converts a codeblock containing a dot graph/digraph to an image and links that image.

The name of the produced file is generated from the hash of the code.

The image gets a class of 'dot' to make special styling possible.

You can give the image a caption with the attribute 'caption'.

The image is saved in the current folder by default. To change this, either set the
attribute 'folder' in the codeblock or globaly in the metadata block with the field
'dot-image-folder'.

The default image format is png. This can be changed by either an attribute
to the codeblock named 'format' or for the whole document in the metadata block with
a field named 'dot-image-format'.
"""
import subprocess
import hashlib
import os
from pandoc_styles import run_pandoc_styles_filter, CodeBlock


def dot(self):
    fmt = self.attributes.get("format") or self.get_metadata("dot-image-format", "png")
    caption = self.attributes.get("caption", "")
    file_name = hashlib.md5(self.text.encode('utf-8')).hexdigest()[:9]
    file_name = f"{file_name}.{fmt}"
    folder = self.attributes.get("folder") or self.get_metadata("dot-image-folder")
    if folder:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, file_name)

    if not os.path.isfile(file_name):
        subprocess.run(f"dot -T{fmt} -o{file_name}", input=self.text, encoding="utf-8")
    return f"![{caption}]({file_name}){{.dot}}"


if __name__ == "__main__":
    run_pandoc_styles_filter(dot, CodeBlock, "dot")
