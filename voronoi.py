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
        if len(test_points) < args.num_grains:
            radius *= 0.95
        else:
            break
    
    chosen_points = np.random.choice(
        np.arange(len(test_points)),
        args.num_grains,
        replace=False
    )
    
    points = test_points[chosen_points, :]
    if args.grain_location_file is not None:
        point_set = pv.PointSet(points).cast_to_unstructured_grid()
        point_set.point_data['values'] = np.arange(len(points)) 
        point_set.save(args.grain_location_file)
 
    search_tree = KDTree(points)
    
    x = np.arange(args.resolution, dtype=float) / (args.resolution - 1)
    grid = np.stack(np.meshgrid(x, x, x), axis=-1)  # (r, r, r, 3)
    regions = search_tree.query(grid)[1]

    data = pv.PointSet(grid.reshape(-1, 3)).cast_to_unstructured_grid()
    data.point_data['values'] = regions.flatten()
    data.save(args.output_file)
    print(f'Saved {args.resolution}^3 image in {args.output_file}')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('num_grains', type=int)
    parser.add_argument('resolution', type=int)
    parser.add_argument('output_file')
    parser.add_argument('--grain_location_file', default=None)
    main(parser.parse_args())

