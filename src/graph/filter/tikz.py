#!/usr/bin/env python3

"""
Converts a codeblock containing tikz tex code to an image and links that image if a
non pdf or non latex format should be made.

The name of the produced file is generated from the hash of the code.

The image gets a class of 'tikz' to make special styling possible.

You can give the image a caption with the attribute 'caption'.

You can specify the width, height and dpi with the corresponding attributes, just like pandoc image attributes.

You can give extra packages that should be imported with the
"tikz-packages" metadata field (as a list) or directly in the code.

The image is saved in the current folder by default. To change this, either set the
attribute 'folder' in the codeblock or globaly in the metadata block with the field
'tikz-image-folder'.

The default image format is png. This can be changed by either an attribute
to the codeblock named 'format' or for the whole document in the metadata block with
a field named 'tikz-image-format'.

You can give the path to magick with "magick-path". Defaults to "magick convert" on 
windows and "convert" on other os.

You can give the attribute "magick-convert-src" and magick-convert-dst image magick
options to change how the image is created. The defaults use 300dpi and trim for src
and highest quality for dst.

With the attribute "pdf=true" the tikz images will be processed in pdfs too.

Some tikz libraries use lualatex, so that is used by default. But you can set any TeX
engine you like with the metadata field "tikz-engine".

Needs image magick, pdflatex/lualatex and ghostscript
"""
import hashlib
import os
import shutil
from tempfile import TemporaryDirectory
from pandoc_styles import (run_pandoc_styles_filter, CodeBlock, run_process, file_write,
                           change_dir, make_list, LATEX)


def tikz(self):
    caption = self.attributes.get("caption", "")
    if self.fmt == LATEX and not self.attributes.get("pdf"):
        if caption != "":
            return [
                "\\begin{figure}\n" +
                self.text +
                f"\n\\caption{{{caption}}}\n\\end{{figure}}"
            ]
        return [self.raw_block(self.text)]
    
    width = f'width={self.attributes.get("width")}' if self.attributes.get("width") else ""
    height = f'height={self.attributes.get("height")}' if self.attributes.get("height") else ""
    dpi = f'width={self.attributes.get("dpi")}' if self.attributes.get("dpi") else ""
    magick_path = self.get_metadata("magick-path",
                                    "magick convert" if os.name == "nt" else "convert")
    magick_convert_src = self.attributes.get("magick-convert-src") or \
        self.get_metadata("tikz-magick-convert-src", "-density 300 -trim")
    magick_convert_dst = self.attributes.get("magick-convert-dst") or \
        self.get_metadata("tikz-magick-convert-dst", "-quality 100")
    hash_src = self.text + magick_convert_src + magick_convert_dst
    file_name_hash = hashlib.md5(hash_src.encode('utf-8')).hexdigest()[:9]
    fmt = self.attributes.get("format") or self.get_metadata("tikz-image-format", "png")
    file_name = file_path = f"{file_name_hash}.{fmt}"
    folder = self.attributes.get("folder") or self.get_metadata("tikz-image-folder")
    latex_engine = self.get_metadata("tikz-engine", "lualatex")
    if folder:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, file_name)

    if not os.path.isfile(file_path):
        packages = "\n".join(f"\\usetikzlibrary{{{p}}}"
                             for p in make_list(self.get_metadata("tikz-packages", [])))
        gdpackages = "\n".join(f"\\usegdlibrary{{{p}}}"
                             for p in make_list(self.get_metadata("tikz-gdpackages", [])))
        tex_code = f"""\\documentclass{{standalone}}
                       \\usepackage{{tikz}}
                       {packages}
                       {gdpackages}
                       \\begin{{document}}
                       {self.text}
                       \\end{{document}}
                    """

        file_path_abs = os.path.abspath(file_path)
        with TemporaryDirectory() as tmpdir:
            with change_dir(tmpdir):
                temp_file = file_write(f"{file_name_hash}.tex", tex_code)
                run_process(f'{latex_engine} {temp_file}', True)
                run_process(f'{magick_path} {magick_convert_src} {file_name_hash}.pdf '
                            f'{magick_convert_dst} {file_name}', True)
                shutil.move(file_name, file_path_abs)
    return f"![{caption}]({file_path}){{.tikz {width} {height} {dpi}}}"


if __name__ == "__main__":
    run_pandoc_styles_filter(tikz, CodeBlock, ["tikz"])
