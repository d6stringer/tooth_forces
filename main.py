import imageio
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

path = 'C:/Users/dwoodson/PycharmProjects/tooth_forces/'
# Get data from excel file
data_from_file = pd.read_excel("data-1.xlsx")
data = data_from_file.values.tolist()

data2_from_file = pd.read_excel("data-1.xlsx")
data2 = data2_from_file.values.tolist()

def rotate(vector, angle):
    """
    Returns a vector rotated by a specified angle in degrees.
    Keyword arguments:
        vector -- numpy array in the form [[a],[b]]
        angle -- angle in degrees
    """
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    r = np.array(((c, -s), (s, c)))
    return r.dot(vector)

def buccal_adjust_vectors(list_a, list_b):
    """
    Returns a list of numpy array vectors in the form array[[a],[b]],...
    where the origin of those vectors has been rotated to the orientation
    of each tooth. The lists must be the same length
    Keyword arguments:
        list_a -- any list meant to represent one dimension of a vector quantity
        list_b -- any list meant to represent one dimension of a vector quantity
    """
    vectors = []
    for i in range(len(list_a)):
        vectors.append(rotate(np.array([[list_a[i]], [list_b[i]]]), tooth_angles[i]))
    return vectors

def plot_vectors(vectors, color, ax):
    """
    Plots a list of numpy vectors as quivers (arrows).
    Keyword arguments:
    vectors -- list of 2D numpy vectors you want to plot
    color -- any base or CSS color
    title -- title of the graph
    """
    vector_scale = 0.06  # smaller is bigger, of course
    vector_units = 'xy'  # see quiver docs
    for i in range(len(vectors)):
        ax.quiver(teeth_x_locations[i], teeth_y_location[i], vectors[i][0], vectors[i][1], color=color,
                  scale=vector_scale, units=vector_units)
    return None

def make_plots(data_a, data_b, data_c):
    filenames = []

    for i in range(len(data_b)):
        img = plt.imread("teef.png")
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.set_title(i)
        ax.axis('off')

        vectors = buccal_adjust_vectors(data_a, data_b[i]) #to make composite vectors you'll have to change "data_a" here, for zeros or ones you can't use indexing.
        vectors2 = buccal_adjust_vectors(data_c[i], data_a)
        plot_vectors(vectors, 'r', ax)
        plot_vectors(vectors2, 'g', ax)

        filename = f'plot{i}.png'
        plt.savefig(filename)
        #add extra frames to slow it down
        for i in range(2):
            filenames.append(filename)
        plt.close()
    return filenames

def make_gif(filenames):
    for k in range(3):
        filenames.append(filenames[-1])

    with imageio.get_writer('forces.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    return None

def delete_files(filenames):
    for filename in filenames:
        if filename in filenames:
            os.remove(filename)
            filenames = list(filter((filename).__ne__, filenames))
    return None


# Not in use but I wrote it out so I'm not deleting it. All lists are in this order.
teeth_ids = ['1-7', '1-6', '1-5', '1-4', '1-3', '1-2', '1-1', '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7']

# These are pixel values of the center of each (used) tooth in the image.
teeth_x_locations = [350, 450, 550, 675, 800, 1030, 1325, 1700, 1995, 2225, 2350, 2475, 2575, 2675]
teeth_y_location = [1800, 1400, 1075, 800, 550, 375, 275, 275, 375, 550, 800, 1075, 1400, 1800]
# angle of the tooth, calculated in the helper excel
tooth_angles = [74, 73, 69, 63, 51, 36, 6, -6, -36, -51, -63, -69, -73, -74]
# some zeros and ones that are helpful for cartesian components, testing
zeros = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ones = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# These were test forces, not used in gif creation
x_forces = [-0.694596132, 0.009485834, -0.172768466,0.397566218, 0.318068345, -0.002802854,-0.004696418, 0.218346237, 0.12512199, -0.653732911, -0.133060316, -2.061648456, -0.023922405, 2.32082011]
y_forces=[0.035842987,0.073104122,0.074166366,0.014452806,0.029474532,0.001455107,-0.00519754,-0.061025126,0.021494228,-0.026219908,0.026614435,0.001354274,-0.06099534,-0.0188011]
m_x = [1.318218459,-6.383277892,-2.204456464,0.563085942,1.251697703,-1.045772825,12.05529395,15.70611027,0.159313544,5.658746342,-2.605700592,0.054121096,-1.76405143,1.342880227]


#These just calculate and plot unit vectors adjusted, uncomment to use
# x_vectors = buccal_adjust_vectors(ones, zeros)
# y_vectors = buccal_adjust_vectors(zeros, ones)
# plot_vectors(x_vectors, 'peachpuff', 'fun')
# plot_vectors(y_vectors, 'chartreuse', '')
# plt.show()

if __name__ == "__main__":
    files = make_plots(zeros, data, data2)
    make_gif(files)
    delete_files(files)

