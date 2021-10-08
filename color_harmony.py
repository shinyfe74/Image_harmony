import cv2, numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter
from scipy import stats
from scipy.signal import find_peaks

def image_harmony(image_path, threshold = 0.005, hue_distance = 15, harmony_graph=False):
    #read image
    start_time = time.time()
    image = cv2.imread(image_path)

    #convert bgr to hsv
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #convert image to 1D array
    image_array = np.reshape(image, (-1, 3))

    #get hue
    hue_arr = image_array[:,0]
    hue_counter = Counter(hue_arr)
    
    #calculate normalized frequency
    total = sum(hue_counter.values())
    normalized_frequency = {k: v / total for k, v in hue_counter.items()}

    #make gaussian_kde
    gaussian_kde = stats.kde.gaussian_kde(hue_arr, bw_method='silverman')
    #make linespace for kde (in opencv, hue has range(0, 180))
    x_grid = np.linspace(0, 180, 360)  #index is hue degree
    peaks, properties = find_peaks(gaussian_kde(x_grid), height=threshold, distance=hue_distance)

    #find 1st peak
    peak1_id = np.argmax(properties["peak_heights"])
    peak1 = int(x_grid[peaks[peak1_id]]*2)
    peak1_xy = [peak1, properties["peak_heights"][peak1_id]]

    #find 2dn peak
    #if has no peak 2, harmoney == 0
    if len(peaks) < 2:
        peak2_xy = ['None', 'None']
        harmony_opp = "Color Inharmonic"

    else:
        peak2_id = np.argsort(properties["peak_heights"])[-2]
        peak2 = int(x_grid[peaks[peak2_id]]*2)
        peak2_xy = [peak2, properties["peak_heights"][peak2_id]]

        #calculate harmonry
        harmony_div = abs(peak1 - peak2)

        if harmony_div > 180:
            harmony_opp = abs(360-harmony_div)
        else:
            harmony_opp = harmony_div

        #if peaks close to (0, 360), recalculate harmony
        if (harmony_opp < hue_distance) :
            if len(peaks) < 3:
                peak2_xy = ['None', 'None']
                harmony_opp = "Color Inharmonic"
            else:
                peak2_id = np.argsort(properties["peak_heights"])[-3]
                peak2 = int(x_grid[peaks[peak2_id]]*2)
                peak2_xy = [peak2, properties["peak_heights"][peak2_id]]

                harmony_div = abs(peak1 - peak2)

                if harmony_div > 180:
                    harmony_opp = abs(360-harmony_div)
                else:
                    harmony_opp = harmony_div

    #draw graph
    if harmony_graph:
        fig = plt.figure()
        ax = plt.gca()
        ax.bar(normalized_frequency.keys(), normalized_frequency.values())
        ax.set_xlabel("Hue", size=6)
        ax.set_xlim(xmin = 0, xmax = 180)
        ax.set_ylabel("Normalized Frequency", size=6)
        ax.plot(x_grid, gaussian_kde(x_grid), 'r-', label='Gaussian_kde')
        ax.plot(x_grid[peaks[peak1_id]], properties["peak_heights"][peak1_id], 'x', ms=10, label=" 1st peak ({0},{1:.3f})".format(peak1, properties["peak_heights"][peak1_id]))
        if (harmony_opp != 0):
            ax.plot(x_grid[peaks[peak2_id]], properties["peak_heights"][peak2_id], 'x', ms=10, label=" 2nd peak ({0},{1:.3f})".format(peak2, properties["peak_heights"][peak2_id]))
        ax.legend(loc='upper right')
        fig.savefig('./color_harmony.jpg', dpi=400)


    completion_time = time.time() - start_time
    return harmony_opp, peak1_xy, peak2_xy, completion_time


print(image_harmony('./Lenna.png', threshold=0.005, hue_distance=15, harmony_graph=False))


