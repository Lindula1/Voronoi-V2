import math
import random

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as patch
from numpy import ndarray

from random_poly import generate_inscribed_square


class DelaunayV2:
    def __init__(self, points, grid=False):
        self.grid = grid
        self.seed_points = points
        self.bin_grid = None

    def triangulate(self, points=None):
        if points is None:
            points = self.seed_points
        normalised_points = self.normalize_points(points)
        bin_numbers = self.generate_bins_nums_2d(points, points)
        sorted_points = self.sort_bins(points, bin_numbers)
        binned_points = self.bin_points(sorted_points, np.sort(bin_numbers))

        return binned_points

    def generate_bin_grid(self, bin_indices, points):
        grid_n = max(np.max(bin_indices, axis=1) + 1)
        max_reach = max(np.max(points, axis=1))
        r = (max_reach/grid_n)/2
        polygons = []
        for i in range(1, grid_n*2, 2):
            for j in range(1, grid_n*2, 2):
                center = [i*r, j*r]
                polygons.append(generate_inscribed_square(center, r))

        self.bin_grid = np.array(polygons)


    def normalize_points(self, points):
        """
        Normalize seed points so they lie between 0 and 1.
        Done with a uniform scaling to ensure all points
        retain their positions.
        """
        max_points = np.max(points, axis=0) - np.min(points, axis=0)
        res = (points - np.min(points, axis=0)[np.newaxis,:])/max_points[np.newaxis,:]
        return res

    def bin_points(self, points, bins):
        # bin_arr, bin_sizes = np.unique(bins, return_counts=True)
        point_bins = [[] for _ in range(max(bins))]

        for i, item in enumerate(bins):
            point_bins[item-1].append(points[i])

        for k, arr in enumerate(point_bins):
            point_bins[k] = np.array(arr)
            # print(k, np.array(arr))

        return point_bins

    def generate_bins_nums_2d(self, norm_points, raw_points):
        N = norm_points.shape[0] # point number
        n = int(np.sqrt(N))
        bin_indices = ((0.99*n*norm_points)/np.max(norm_points, axis=0)[np.newaxis, :]).astype(int)

        if self.grid:
            self.generate_bin_grid(bin_indices, raw_points)

        bins = np.zeros(N, dtype=int)
        for i in range(N):
            bins[i] = bin_indices[i,1] * n + bin_indices[i,0] + 1 if bin_indices[i,1] % 2 == 0 else (bin_indices[i,1] + 1)* n - bin_indices[i,0]

        return bins

    def sort_bins(self, points, bin_numbers):
        sorted_points = knuth_counting_sort_numpy(points, bin_numbers)
        return sorted_points


def knuth_counting_sort_numpy(coords: np.ndarray, ranks: np.ndarray) -> np.ndarray:
    """
    ---Produced using AI--- (I'm lazy)
    Knuth's Counting Sort (Algorithm C) for NumPy arrays.
    ----------------------------------------------------
    Sorts coords based on integer ranks in O(n + k) time.

    Parameters
    ----------
    coords : np.ndarray
        Array of shape (n, 2) with 2D coordinates.
    ranks : np.ndarray
        Array of shape (n,) with integer rank values.

    Returns
    -------
    np.ndarray
        Sorted coordinates array (same shape as input).
    """
    n = ranks.size
    if n == 0:
        return coords

    min_rank = ranks.min()
    max_rank = ranks.max()
    k = max_rank - min_rank + 1

    count = np.zeros(k, dtype=np.int64)
    np.add.at(count, ranks - min_rank, 1)

    count = np.cumsum(count)

    output = np.empty_like(coords)
    for i in range(n - 1, -1, -1):
        r = ranks[i]
        count[r - min_rank] -= 1
        pos = count[r - min_rank]
        output[pos,:] = coords[i,:]

    return output


if __name__ == "__main__":
    """Seed Variables"""
    np.random.seed(69)
    random.seed(69)
    seed_point_num = 20

    """Generate Delaunay"""
    seed_points = np.random.uniform(0, 10, (seed_point_num,2))
    delaunay = DelaunayV2(seed_points, True)
    triangulated = delaunay.triangulate()

    colours = [(random.random(), random.random(), random.random()) for i in range(seed_point_num)]

    grid_points = delaunay.bin_grid
    grid = [patch.Polygon(_, fill=False) for _ in grid_points]

    """ Graphing """
    fig, ax = plt.subplots(1, 1)
    # Graphing points
    for l in range(len(triangulated)):
        if len(triangulated[l]) == 0:
            continue
        ax.plot(triangulated[l][:,0], triangulated[l][:,1], "o", color=colours[l])

    # ax.plot(seed_points[:,0], seed_points[:,1], "o")
    # ax.figure(2, figsize=(8,8))
    # ax.plot(triangulated[:,0], triangulated[:,1], "o")

    # Graphing grid
    for f in grid:
        ax.add_patch(f)


    plt.show()