#!/usr/bin/env python3

"""
Converts a codeblock containing a matplotlib plot to an image.

Imports matplot.pyplot as plt and numpy as np for you.

The name of the produced file is generated from the hash of the code.

The image gets a class of 'plot' to make special styling possible.

The image is saved in the current folder by default. To change this, either set the
attribute 'folder' in the codeblock or globaly in the metadata block with the field
'plot-image-folder'.

The default image format is png. This can be changed by either an attribute
to the codeblock named 'format' or for the whole document in the metadata block with
a field named 'plot-image-format'.

Renderer: The renderer used. Defaults to AGG. Is changed depending on format. You can
set it manually for full control. Attribute: "renderer" Global: "plot-renderer"

You can give the image a caption with the attribute 'caption'.

You can make the images transparent. Either with an attribute 'transparent' set to true,
or with the metadata field 'plot-transparent' set to true.

You can show the code with the option .show
"""
import hashlib
import os
from pandoc_styles import run_pandoc_styles_filter, CodeBlock

RENDERER = {"png": "AGG", "ps": "PS", "pdf": "PDF", "svg": "SVG"}

def plot(self):
    width = f'width={self.attributes.get("width")}' if self.attributes.get("width") else ""
    height = f'height={self.attributes.get("height")}' if self.attributes.get("height") else ""
    fmt = self.attributes.get("format") or self.get_metadata("plot-image-format", "png")
    renderer = self.attributes.get("renderer") or self.get_metadata("plot-renderer") or \
               RENDERER[fmt]
    trans = self.attributes.get("transparent") or \
            self.get_metadata("plot-transparent", False)
    show = self.attributes.get("show") or \
           self.get_metadata("plot-show", False)
    caption = self.attributes.get("caption", "")
    hash_src = self.text + "trans" if trans else self.text
    file_name = hashlib.md5(hash_src.encode('utf-8')).hexdigest()[:9]
    folder = self.attributes.get("folder") or self.get_metadata("plot-image-folder")
    if folder:
        file_name = os.path.join(folder, file_name)
        if not os.path.isdir(folder):
            os.makedirs(folder)

    images = []
    cur_file_name = f"{file_name}1.{fmt}"
    if os.path.isfile(cur_file_name):
        i = 1
        while os.path.isfile(cur_file_name):
            images.append(f"![{caption}]({cur_file_name}){{.plot}}")
            i += 1
            cur_file_name = f"{file_name}{i}.{fmt}"
    else:
        local_vars = {}
        # pylint: disable=exec-used
        exec(f"import matplotlib\nimport matplotlib.pyplot as plt\nimport numpy as np\n"
             f"matplotlib.use('{renderer}')\n{self.text}",
             {}, local_vars)
        plt = local_vars["plt"]
        for i in plt.get_fignums():
            plt.figure(i)
            cur_file_name = f"{file_name}{i}.{fmt}"
            plt.savefig(cur_file_name, format=fmt, bbox_inches='tight', transparent=trans)
            images.append(f"![{caption}]({cur_file_name}){{.plot {width} {height}}}")
    images = "\n".join(images)

    if show:
        self.classes.append("python")
        return [self.elem, self.convert_text(images)]
    return images


if __name__ == "__main__":
    run_pandoc_styles_filter(plot, CodeBlock, ["plot", "plt"])
