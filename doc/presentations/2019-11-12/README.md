## Presentation Template

Fork this project for your presentation if you want to. The template provides a basic `Makefile` including `ggplot` integration and some examples. You are free to edit and extend the scaffold to fit your needs.

You can either use [TeXstudio](https://www.texstudio.org/) or any other IDE/editor but the `ggplot` integration and `minted` configuration will only work when building using the Makefile

### Minted

[minted](https://ctan.org/pkg/minted) is a LaTeX package that facilitates expressive syntax highlighting using the Pygments library. The package also provides options to customize the highlighted source code output using `fancyvrb`.
If you want to use it without the Makefile you will likely need to remove the `[outputdir=latex.out]` option from the `main.tex` file.

### ggplot

[ggplot2](https://ggplot2.tidyverse.org/) is a system for declaratively creating graphics for the statistical programming language `R`, based on The Grammar of Graphics. You provide the data, tell ggplot2 how to map variables to aesthetics, what graphical primitives to use, and it takes care of the details.
You can find some examples of usage and the integration in te `R` folder within this project and additional examples online, e.g. [here](https://evamaerey.github.io/ggplot_flipbook/ggplot_flipbook_xaringan.html#1).
To replace the given examples with your own remember to set the `PLOT_PREFIX` in the Makefile and name the files accordingly (`PLOT_PREFIXfilename.R`).

### Building
****
If you installed `R`, `ggplot` and `minted` correctly you can build the example and your own project using `make` in the source director. The makefile provides multiple targets

```
make
```
Builds the presentation pdf.

```
make clean
```
Removes all generated files.

```
make Plots
```
Builds all ggplot plots to pdf files.

```
make view
```
Opens the presentation pdf.

```
make printPlotNames
```
Prints all plot names (helpful to ensure all own plots are correctly included).
