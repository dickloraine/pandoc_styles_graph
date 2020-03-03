# pandoc_styles: novel

## About

This is a stylepack for [pandoc_styles](https://github.com/dickloraine/pandoc_styles).
You need pandoc-styles in order to make use of this project.

This stylepack converts dot, matplot, mermaid, plantuml and tikz code blocks into images. This way it is possible to write graphs, plots and diagrams in markdown.

## Prerequisites

[pandoc-styles](https://github.com/dickloraine/pandoc_styles) and its dependencies.

## Installation

Install with:

    pandoc-styles-tools import novel -u https://github.com/dickloraine/pandoc_styles_novel/releases/latest/download/novel.zip


## Documentation

You write the code for the image inside a codeblock with the name of the engine used.

You can often give some options for the rendering. If the option should be used only for the current image, just give it as an attribute to the codeblock. If it should be used for all images, you can add it to the metadata by prefixing the option with the engines name.

The images are saved in the current folder by default. This can be changed in the metadata with `engine-image-folder`, where engine is the engine that should use that folder. The image format is per default png, but can be changed for some engines. All images get a class with the name of the engine to make styling possible. Images can get a caption with the caption attribute.

Here is an example of a mermaid graph with custom width and a caption. Transparent background and the image folder are set in the metadata:

    ---
    mermaid-image-folder: ./images
    mermaid-background: transparent
    ---

    ``` {.mermaid caption="some graph" width=400}
    graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
    ```

### dot

**Requirements:**

- [graphviz](https://www.graphviz.org/)

**Possible formats:**

- [many](https://graphviz.gitlab.io/_pages/doc/info/output.html)

**Name:**

- dot

### matplot

**Requirements:**

- python
- matplotlib
- numpy

**Possible formats:**

- png
- svg
- pdf

**Name:**

- plot
- plt

This imports `matplotlib.pyplot` as `plt` and `numpy` as `np`. You have to use these imports for it to work.

**Options:**

renderer
  : The renderer used. Per default chooses one fitting the format.

transparent
  : Image background is transparent.

show
  : If set to true, shows the code in addition to the image.

**Example:**

    ``` {.python .plot}
    from matplotlib.colors import BoundaryNorm
    from matplotlib.ticker import MaxNLocator

    # make these smaller to increase the resolution
    dx, dy = 0.05, 0.05

    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(1, 5 + dy, dy),
                    slice(1, 5 + dx, dx)]

    z = np.sin(x)**10 + np.cos(10 + y*x) * np.cos(x)

    # x and y are bounds, so z should be the value *inside* those bounds.
    # Therefore, remove the last value from the z array.
    z = z[:-1, :-1]
    levels = MaxNLocator(nbins=15).tick_values(z.min(), z.max())

    # pick the desired colormap, sensible levels, and define a normalization
    # instance which takes data values and translates those into levels.
    cmap = plt.get_cmap('PiYG')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    fig, (ax0, ax1) = plt.subplots(nrows=2)

    im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm)
    fig.colorbar(im, ax=ax0)
    ax0.set_title('pcolormesh with levels')

    # contours are *point* based plots, so convert our bound into point
    # centers
    cf = ax1.contourf(x[:-1, :-1] + dx/2.,
                    y[:-1, :-1] + dy/2., z, levels=levels,
                    cmap=cmap)
    fig.colorbar(cf, ax=ax1)
    ax1.set_title('contourf with levels')

    # adjust spacing between subplots so `ax1` title and `ax0` tick labels
    # don't overlap
    fig.tight_layout()
    ```

### mermaid

**Requirements:**

- [mermaid-cli](https://github.com/mermaidjs/mermaid.cli)

**Possible formats:**

- png
- svg
- pdf

**Name:**

- mermaid
- mmd

**Options:**

width
  : The width of the image. Just a number of pixels.

height
  : The height of the image. Just a number of pixels.

background
  : The background color.

### plantuml

**Requirements:**

- [plantuml](https://plantuml.com/)

**Possible formats:**

- png

**Name:**

- plantuml
- puml

**Options:**

plantuml-command
  : Global option to set the command line command for plantuml, if it is not just plantuml.

### tikz

**Requirements:**

- pdflatex
- ghostscript
- [image magick](https://imagemagick.org/index.php)

**Possible formats:**

- all supported by image magick

**Name:**

- tikz

You can use the tikz latex package even outside pdf output. If the output is a pdf, native tikz is used. For other formats, an image is created.

**Options:**

width
  : The width of the image. Needs a unit.

height
  : The height of the image. Needs a unit.

tikz-packages
  : Global setting. A list of tikz-packages used.

pdf
  : If set to true, even in pdfs an image is created

magick-convert-src
  : Expert setting for converting. Default: `-density 300 -trim`

magick-convert-dst
  : Expert setting for converting. Default: `-quality 100`

**Example:**

    ``` tikz
    \begin{tikzpicture}[auto, shorten >=1pt]
    \node[state, accepting] at (4,4)    (s)  {$s$};
    \node[state]            at (0,0)    (0)  {$0$};
    \node[state]            at (8,0)    (1)  {$1$};
    \path[->] (s)  edge        node {0, u}           (0)
            (s)  edge        node {1, u}           (1)
            (0)  edge [loop below]        node {0, g}           (0)
            (0)  edge [bend left]        node {1, u}           (1)
            (1)  edge [bend left]         node {0, u}           (0)
            (1)  edge [loop below]       node {1, g}           (1);
    \end{tikzpicture}
    ```
