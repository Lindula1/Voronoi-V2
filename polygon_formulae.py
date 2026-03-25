import numpy as np
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as patch

def poly_signed_area_2d(vertices):
    x = vertices[:, 0]
    y = vertices[:, 1]
    res = x[:-1] * y[1:] - x[1:] * y[:-1]
    return np.abs(np.sum(res))*0.5

def gen_circum_center(vertices):
    a, b, c = vertices
    d = 2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
    u_x = (1/d)*(np.sum(a**2)*(b[1]-c[1])+np.sum(b**2)*(c[1]-a[1])+np.sum(c**2)*(a[1]-b[1]))
    u_y = (1/d)*(np.sum(a**2)*(c[0]-b[0])+np.sum(b**2)*(a[0]-c[0])+np.sum(c**2)*(b[0]-a[0]))
    return u_x, u_y

def centroid_distance(vertices, centroid):
    a, b = centroid
    x, y = vertices[0][0], vertices[0][1]
    distance = np.sqrt((x-a)**2+(y-b)**2)
    return distance

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
    import random_poly as poly_gen
    np.random.seed(67)
    # polygon = np.random.uniform(0, 2,(7,2))
    # polygon = np.array([
    #     [0, 0],
    #     [5, 0],
    #     [4, 6],
    #     [0, 4],
    #     [0, 0]
    # ])
    polygon = poly_gen.generate_polygon(center=(0, 0),
                                avg_radius=20,
                                irregularity=0.35,
                                spikiness=0.2,
                                num_vertices=3)
    polygon = np.array(polygon)
    # area = poly_signed_area_2d(polygon)
    # centroid = poly_centroid_2d(polygon, area)
    # radius = centroid_distance(polygon, centroid)
    # print(centroid)
    # polygon = np.array([[3,2],[1,4],[5,4]])
    centroid = gen_circum_center(polygon)
    print(centroid)
    radius = centroid_distance(polygon, centroid)

    circle = patch.Circle(centroid, radius, color='r', fill=False)

    fig, ax = plt.subplots(1,1)
    p = Polygon(polygon, closed=True)
    ax.add_patch(circle)
    ax.add_patch(p)
    ax.plot(centroid[0], centroid[1], "ro")
    plt.ylim([-50, 50])
    plt.xlim([-50, 50])
    plt.show()