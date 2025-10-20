from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

class DelaunayV2:
    def __init__(self, points):
        self.seed_points = points

    def triangulate(self, points=None):
        if points is None:
            points = self.seed_points
        normalised_points = self.normalize_points(points)
        lawson_bins = self.generate_bins(normalised_points)

    def normalize_points(self, points):
        """
        Normalize seed points so they lie between 0 and 1.
        Done with a uniform scaling to ensure all points
        retain their positions.
        """
        max_points = np.max(points, axis=1) - np.min(points, axis=1)
        res = (points - np.min(points, axis=1)[:, np.newaxis])/max_points[:, np.newaxis]
        return res

    def generate_bins(self, points):
        n = points.shape[1]
        bin_indices = (0.99*n*points/np.max(points, axis=1)[:, np.newaxis]).astype(int)
        print(bin_indices)
        bins = np.zeros(n)
        for i in range(n):
            bins[i] = bin_indices[1,i] * n + bin_indices[0,i] + 1 if bin_indices[1,i] % 2 == 0 else (bin_indices[1,i] + 1)* n - bin_indices[0,i]
        print(bins)
        return None



if __name__ == "__main__":
    np.random.seed(0)
    seed_points = np.random.uniform(0, 10, (2,13))
    # print(seed_points)
    delaunay = DelaunayV2(seed_points)
    delaunay.triangulate()