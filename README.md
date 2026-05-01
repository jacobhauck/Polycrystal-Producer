# Polycrystal-Producer
Generate and export random polycrystal grain structures.

## Usage
There is a single command to generate structures, which is used as follows.
```
python voronoi.py NUMBER_OF_GRAINS RESOLUTION OUTPUT_FILE [--grain_locations_file GRAINS_FILE]
```
The `NUMBER_OF_GRAINS` argument is the number of grains in the generated polycrystal, and `RESOLUTION` is the number of points in each direction of the discrete grid used to save the generated stucture. The output is saved in `OUTPUT_FILE`, which should be a `.vtu` file. If desired, the locations of the grains (see Algorithm section) can also be saved by specifying the optional `GRAINS_FILE` argument, which should also be a `.vtu` file.

## Algorithm
Polycrystal grain structures are generated using the following two-step approach.

1. Sample $n$ grain locations $\{x_i\}_{i=1}^n$, where $x_i \in [0,1]^3$ using Poisson disk sampling, which ensures that $\|x_i - x_j\| >r$ if $i \ne j$, where the radius $r$ is a parameter that you choose to determine how small and how many grains you want. A particular number of grains $n$ can be specified as follows. We can draw a ball of radius $\frac{r}{2}$ around each $x_i$, and each ball is disjoint. The total volume is then $1 > n\frac{4\pi (r/2)^3}{3}$, which gives $r<2\left(\frac{3}{4\pi n}\right)^\frac{1}{3}$. Attempt to perform Poisson disk sampling with this $r$ and randomly select $n$ of the points sampled. If fewer than $n$ are sampled, set $r = 0.9r$ and repeat until at least $n$ points are sampled (though usually you get more than $n$ on the first try).
2. Given the set $\{x_i\}$ of grain locations, generate the grain geometry by simply constructing the Voronoi diagram. In other words, $x$ belongs to grain $i$ if and only if $x$ is closest to point $x_i$. Discretizing $[0,1]^3$ using a uniform rectangular grid, we can calculate which region each grid point belongs to by finding the point $x_i$ that it is closest to.
