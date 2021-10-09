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

    peaks_x = []
    peaks_y = []
    for i in range(len(peaks)):
        peaks_x.append(int(x_grid[peaks[i]]*2))
        peaks_y.append(properties["peak_heights"][i])


    #find 1st peak
    if len(peaks) > 0:
        sort_peak_y = np.argsort(properties["peak_heights"])
        peak1_x = int(x_grid[peaks[sort_peak_y[-1]]]*2)
        raw_peak1_x = int(x_grid[peaks[sort_peak_y[-1]]])
        peak1_y = properties["peak_heights"][sort_peak_y[-1]]
        peak1_xy = [peak1_x, peak1_y]

        #find 2nd peak
        #if has no peak 2, harmoney == 0
        sort_peak_y = np.delete(sort_peak_y, [-1])

        peak2_x = 'None'
        peak2_y = 'None'
        harmony = "Color Inharmonic"

        while len(sort_peak_y) > 0:
            temp_peak2_x = int(x_grid[peaks[sort_peak_y[-1]]]*2)
            temp_raw_peak2_x = int(x_grid[peaks[sort_peak_y[-1]]])
            temp_peak2_y = properties["peak_heights"][sort_peak_y[-1]]

            harmony_div = abs(peak1_x - temp_peak2_x)
            
            if harmony_div > 180:
                temp_harmony = abs(360-harmony_div)
            else:
                temp_harmony = harmony_div

            #if peaks close to (0, 360), recalculate harmony
            if (temp_harmony < hue_distance):
                sort_peak_y = np.delete(sort_peak_y, [-1])
            else:
                peak2_x = temp_peak2_x
                raw_peak2_x = temp_raw_peak2_x
                peak2_y = temp_peak2_y
                harmony = temp_harmony
                break

        peak2_xy = [peak2_x, peak2_y]

    else:
        peak1_xy = ['None', 'None']
        peak2_xy = ['None', 'None']
        harmony = "Color Inharmonic"


    #draw graph
    if harmony_graph:
        fig = plt.figure()
        ax = plt.gca()
        ax.bar(normalized_frequency.keys(), normalized_frequency.values())
        ax.set_xlabel("Hue", size=6)
        ax.set_xlim(xmin = 0, xmax = 180)
        ax.set_ylabel("Normalized Frequency", size=6)
        ax.plot(x_grid, gaussian_kde(x_grid), 'r-', label='Gaussian_kde')
        ax.plot(raw_peak1_x, peak1_y, 'x', ms=10, label=" 1st peak ({0},{1:.3f})".format(peak1_x, peak1_y))
        if (harmony != "Color Inharmonic"):
            ax.plot(raw_peak2_x, peak2_y, 'x', ms=10, label=" 2nd peak ({0},{1:.3f})".format(raw_peak2_x, peak2_y))
        ax.legend(loc='upper right')
        fig.savefig('./color_harmony.jpg', dpi=400)


    completion_time = time.time() - start_time
    return harmony, peak1_xy, peak2_xy, peaks_x, peaks_y, completion_time


print(image_harmony('./Lenna.jpg', threshold=0.005, hue_distance=30, harmony_graph=True))
