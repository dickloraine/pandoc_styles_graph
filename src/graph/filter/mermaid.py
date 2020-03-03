"""
Converts a codeblock containing mermaid code to an image and links that image.

The name of the produced file is generated from the hash of the code.

The image gets a class of 'mermaid' to make special styling possible.

You can give the image a caption with the attribute 'caption'.

The image is saved in the current folder by default. To change this, either set the
attribute 'folder' in the codeblock or globaly in the metadata block with the field
'mermaid-image-folder'.

The default image format is png. This can be changed by either an attribute
to the codeblock named 'format' or for the whole document in the metadata block with
a field named 'mermaid-image-format'. png, svg and pdf are possible.

width, height, background can be specified with the respective attributes or globaly with
mermaid-width, mermaid-height, mermaid-background.
"""
import hashlib
import os
from pandoc_styles import run_pandoc_styles_filter, CodeBlock, run_process, file_write


def mermaid(self):
    fmt = self.attributes.get("format") or \
          self.get_metadata("mermaid-image-format", "png")
    wid = self.attributes.get("width") or self.get_metadata("mermaid-width", "800")
    hei = self.attributes.get("height") or self.get_metadata("mermaid-height", "600")
    bg = self.attributes.get("background") or \
         self.get_metadata("mermaid-background", "white")
    file_name_hash = hashlib.md5(self.text.encode('utf-8')).hexdigest()[:9]
    file_name = f"{file_name_hash}.{fmt}"
    folder = self.attributes.get("folder") or self.get_metadata("mermaid-image-folder")
    caption = self.attributes.get("caption", "")
    if folder:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, file_name)

    if not os.path.isfile(file_name):
        temp_file = file_write(f"{file_name_hash}.mmd", self.text)
        run_process(f'mmdc -i {temp_file} -o "{file_name}" -w {wid} -H {hei} -b {bg}',
                    shell=True)
        os.remove(temp_file)
    return f"![{caption}]({file_name}){{.mermaid}}"


if __name__ == "__main__":
    run_pandoc_styles_filter(mermaid, CodeBlock, ["mermaid", "mmd"])
