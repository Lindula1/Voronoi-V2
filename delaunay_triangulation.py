import math
import random

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as patch
import numpy.typing as npt

from random_poly import generate_inscribed_rectangle_sym
from polygon_formulae import gen_circum_center

def knuth_counting_sort_numpy(coords: npt.NDArray, ranks: npt.NDArray) -> np.ndarray:
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

"""Depreciated until further development"""
def __generate_bin_indices(norm_points : npt.NDArray) -> np.ndarray:
    """
    :param norm_points:
    :return:
    :rtype:
    """
    n_points = norm_points.shape[0]  # point number
    n = int(np.sqrt(n_points))
    res = ((0.99 * n * norm_points) / np.max(norm_points, axis=0)[np.newaxis, :]).astype(int)

    return res


def _normalize_points(points : npt.NDArray) -> np.ndarray:
    """
    :param points:
    :return:
    Normalize seed points so they lie between 0 and 1.
    Done with a uniform scaling to ensure all points
    retain their positions.
    """
    max_points = np.max(points, axis=0) - np.min(points, axis=0)
    res = (points - np.min(points, axis=0)[np.newaxis,:])/max_points[np.newaxis,:]

    return res


def _bin_points(points : np.ndarray, bins : list[int] | np.ndarray) -> npt.ArrayLike:
    """
    :param points:
    :param bins:
    :return:
    """
    point_bins = [[] for _ in range(max(bins))]

    for i, item in enumerate(bins):
        point_bins[item-1].append(points[i])

    for k, arr in enumerate(point_bins):
        point_bins[k] = np.array(arr)

    return point_bins


def _sort_bins(points : npt.NDArray, bin_numbers : npt.NDArray) -> np.ndarray:
    """
    :param points:
    :param bin_numbers:
    :return:
    """
    sorted_points = knuth_counting_sort_numpy(points, bin_numbers)
    return sorted_points

def _generate_bin_indices_2d(points):
    num_points = points.shape[0]
    n = int(np.sqrt(num_points))
    return ((0.99 * n * points) / np.max(points, axis=0)[np.newaxis, :]).astype(int)


class DelaunayV2:
    def __init__(self, points : npt.NDArray, grid=False):
        """
        :param points:
        :type points:
        :param grid:
        :type grid:
        """
        self.grid = grid
        self.seed_points = points
        self.bin_grid = None

    def triangulate(self, points : npt.NDArray = None):
        """
        :param points:
        :type points:
        :return:
        :rtype:
        """
        if points is None:
            points = self.seed_points

        normalised_points = _normalize_points(points)
        bin_indices = _generate_bin_indices_2d(normalised_points)
        bin_numbers = self.generate_bins_nums_2d(bin_indices, points)
        sorted_points = _sort_bins(points, bin_numbers)
        binned_points = _bin_points(sorted_points, np.sort(bin_numbers))

        current_point = [0,0]
        polygons = []

        while True:
            triangle = self.__next_triangle(binned_points, current_point)
            if triangle is None:
                break
            polygons.append(triangle[0])
            current_point = triangle[1]

        return binned_points, polygons

    def gen_triangle(self, bin_id, bin_num, binned_points):
        if bin_num > len(binned_points) - 1:
            return None

        if bin_id > len(binned_points[bin_num]) - 1:
            return None
        
        res = []
        while len(res) < 2:



    def __next_triangle(self, point_bins, current_coord):
        res = []

        def __next_triangle_aux(point_bins, current_coord, res):

            if len(res) > 2:
                return res, current_coord

            if current_coord[0]+1 > len(point_bins):
                return None

            if point_bins[current_coord[0]].shape[0]-1 < current_coord[1]:
                return __next_triangle_aux(point_bins, [current_coord[0]+1,0], res)

            res.append(point_bins[current_coord[0]][current_coord[1]])

            current_coord = [current_coord[0], current_coord[1] + 1]

            return __next_triangle_aux(point_bins, current_coord, res)

        return __next_triangle_aux(point_bins, current_coord, res)


    def __generate_bin_grid(self, bin_indices : npt.NDArray, points : npt.NDArray) -> None:
        """
        :param bin_indices:
        :type bin_indices:
        :param points:
        :type points:
        :return:
        :rtype:
        """
        grid_n = max(np.max(bin_indices, axis=1)+1)
        max_r_x, max_r_y = np.max(points[:,0])/grid_n, np.max(points[:,1])/grid_n
        print(max_r_x, max_r_y)
        polygons = []
        for i in range(1, grid_n):
            for j in range(1, grid_n):
                center = [i*max_r_x, j*max_r_y]
                polygons.append(generate_inscribed_rectangle_sym(center, max_r_x, max_r_y))

        self.bin_grid = np.array(polygons)

    def generate_bins_nums_2d(self, bin_indices : npt.NDArray, raw_points : npt.NDArray) -> np.ndarray:
        """
        :param bin_indices:
        :type bin_indices:
        :param raw_points:
        :type raw_points:
        :return:
        :rtype:
        """
        num_points = raw_points.shape[0]
        n = int(np.sqrt(num_points))

        if self.grid:
            self.__generate_bin_grid(bin_indices, raw_points)

        bins = np.zeros(num_points, dtype=int)
        for i in range(num_points):
            bins[i] = bin_indices[i,1] * n + bin_indices[i,0] + 1 if bin_indices[i,1] % 2 == 0 else (bin_indices[i,1] + 1)* n - bin_indices[i,0]

        return bins



if __name__ == "__main__":
    """Seed Variables"""
    np.random.seed(69)
    random.seed(69)
    seed_point_num = 14

    """Generate Delaunay"""
    seed_points = np.random.uniform(0, 10, (seed_point_num,2))
    delaunay = DelaunayV2(seed_points)
    triangulated, triangles = delaunay.triangulate()

    colours = [(random.random(), random.random(), random.random()) for i in range(seed_point_num)]

    # grid_points = delaunay.bin_grid
    # grid = [patch.Polygon(_, fill=False) for _ in grid_points]

    """ Graphing """
    fig, ax = plt.subplots(1, 1)
    # Graphing points
    for l in range(len(triangulated)):
        if len(triangulated[l]) == 0:
            continue
        ax.plot(triangulated[l][:,0], triangulated[l][:,1], "o", color=colours[l])

    # Graphing Circum-circles
    triangle_polys = []
    circum_circles = []
    for g in triangles:
        center, radius = gen_circum_center(g, True)
        circum_circles.append(patch.Circle(center, radius, fill=False))
        triangle_polys.append(patch.Polygon(g, fill=False))

    for c in range(len(circum_circles)):
        ax.add_patch(circum_circles[c])
        ax.add_patch(triangle_polys[c])

    # Graphing grid
    # for f in grid:
    #     ax.add_patch(f)


    plt.show()