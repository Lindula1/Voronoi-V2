import numpy as np
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

def poly_signed_area_2d(vertices):
    x = vertices[:, 0]
    y = vertices[:, 1]
    res = x[:-1] * y[1:] - x[1:] * y[:-1]
    return np.abs(np.sum(res))*0.5

def poly_centroid_2d(vertices, signed_area):

    if not np.all(vertices[0] == vertices[-1]):
        vertices = np.vstack([vertices, vertices[0]])

    x = vertices[:, 0]
    y = vertices[:, 1]

    cross = x[:-1] * y[1:] - x[1:] * y[:-1]

    factor = cross[:, np.newaxis]
    res = np.sum((vertices[:-1] + vertices[1:]) * factor, axis=0) / (6 * signed_area)
    return res

if __name__ == "__main__":
    import Random_Poly as poly_gen
    np.random.seed(67)
    # polygon = np.random.uniform(0, 2,(7,2))
    # polygon = np.array([
    #     [0, 0],
    #     [4, 0],
    #     [4, 4],
    #     [0, 4],
    #     [0, 0]
    # ])
    polygon = poly_gen.generate_polygon(center=(250, 250),
                                avg_radius=100,
                                irregularity=0.35,
                                spikiness=0.2,
                                num_vertices=16)
    polygon = np.array(polygon)
    area = poly_signed_area_2d(polygon)
    centroid = poly_centroid_2d(polygon, area)
    print(centroid)

    fig, ax = plt.subplots(1,1)
    p = Polygon(polygon, closed=True)
    ax.add_patch(p)
    ax.plot(centroid[0], centroid[1], "go")
    plt.ylim([0, 400])
    plt.xlim([0, 400])
    plt.show()