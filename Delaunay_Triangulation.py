import random

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from numpy import ndarray


class DelaunayV2:
    def __init__(self, points):
        self.seed_points = points

    def triangulate(self, points=None):
        if points is None:
            points = self.seed_points
        normalised_points = self.normalize_points(points)
        bin_numbers = self.generate_bins_nums_2d(normalised_points)
        sorted_points = self.sort_bins(points, bin_numbers)
        print(sorted_points)
        self.binned_points = self.bin_points(points, bin_numbers)
        print(self.binned_points)

        return sorted_points

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
        N_max = np.max(bins)
        binned_points = [[] for _ in range(N_max)]
        for ind, bin_item in enumerate(bins):
            # np.append(binned_points[bin_item-1], points[ind])
            binned_points[bin_item-1].append(points[ind])

        for j, f in enumerate(binned_points):
            binned_points[j] = np.array(f)

        return binned_points

    def generate_bins_nums_2d(self, points):
        N = points.shape[0] # point number
        n = int(np.sqrt(N))
        bin_indices = ((0.99*n*points)/np.max(points, axis=0)[np.newaxis, :]).astype(int)

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
    np.random.seed(69)
    random.seed(69)
    seed_point_num = 14
    seed_points = np.random.uniform(0, 10, (seed_point_num,2))
    colours = [(random.random(), random.random(), random.random()) for i in range(seed_point_num)]
    # print(seed_points)
    delaunay = DelaunayV2(seed_points)
    triangulated = delaunay.triangulate()
    binned_points = delaunay.binned_points
    plt.figure(1, figsize=(8,8))
    for k in range(len(binned_points)):
        plt.plot(binned_points[k][:,0], binned_points[k][:,1], "o", color=colours[k])
    # plt.plot(seed_points[:,0], seed_points[:,1], "o")
    # plt.figure(2, figsize=(8,8))
    # plt.plot(triangulated[:,0], triangulated[:,1], "o")
    plt.show()