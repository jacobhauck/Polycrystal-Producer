import numpy as np
import argparse
from scipy.stats.qmc import PoissonDisk
from scipy.spatial import KDTree
import pyvista as pv


def main(args):
    radius = 2 * (3/4/np.pi / args.num_grains) ** (1/3)
    while True:
        print(f'Testing radius: {radius}')
        test_points = PoissonDisk(3, radius=radius).fill_space()
        print(f'Found {len(test_points)} points')
        print(f'Pairwise distances')
        dist = np.linalg.norm(test_points[None] - test_points[:, None], axis=-1)
        print(dist)
        print(f'Min dist: {np.min(dist[dist>0])}')
        print(f'Coordinates')
        print(test_points)
        if len(test_points) < args.num_grains:
            radius *= 0.95
        else:
            break
    
    pv.PointSet((args.resolution-1) * test_points).cast_to_unstructured_grid().save('points.vtu')
 
    chosen_points = np.random.choice(
        np.arange(len(test_points)),
        args.num_grains,
        replace=False
    )
    
    points = test_points[chosen_points, :]
    search_tree = KDTree(points)
    
    x = np.arange(args.resolution)
    grid_int = np.stack(np.meshgrid(x, x, x), axis=-1)  # (r, r, r, 3)
    regions = search_tree.query(grid_int / (args.resolution-1))[1]
    
    data = pv.ImageData(dimensions=regions.shape)
    data.point_data['values'] = regions.flatten(order='F')
    data.save(args.output_file)
    print(f'Saved {args.resolution}^3 image in {args.output_file}')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('num_grains', type=int)
    parser.add_argument('resolution', type=int)
    parser.add_argument('output_file')
    main(parser.parse_args())

