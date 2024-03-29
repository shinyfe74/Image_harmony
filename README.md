# Image_harmony
calculate image color harmony by color hue degree

# Library
- numpy
- opencv
- matplotlib.pyplot
- collections Counter
- scipy stats
- scipy.optimize find_peaks


# How to use
You can use module like this

- image_harmony(image_path, threshold(default = 0.005), hue_distance(default = 15) ==> minimum harmony, harmony_graph(default = false))
- ex)  image_harmony('./Lenna.png', threshold=0.005, hue_distance=15, harmony_graph=False)


# Result
This function will return **(Image_harmony, 1st peak xy, 2nd peak xy, peaks x, peaks y, Completion_time)**
 - Image_harmony : The higher value means more harmonious image
- ex)  image_harmony('./Lenna.png', threshold=0.005, hue_distance=15, harmony_graph=False)    
   - > (28, [10, 0.01728678506424689], [342, 0.015386930437978728], [10, 342], [0.01728678506424689, 0.015386930437978728], 0.7515513896942139)

if it has no harmony value
 - image_harmony('./Lenna.png', threshold=0.005, hue_distance=30, harmony_graph=False)   
   - >  ('Color Inharmonic', [10, 0.01728678506424689], ['None', 'None'], [10, 342], [0.01728678506424689, 0.015386930437978728], 0.7615368366241455)

**return graphs**   
1. color harmony graph

<img src="https://user-images.githubusercontent.com/80665546/136632113-99eb5fe1-73e3-4e7d-96fe-7d464b3478e4.png" width="300" height="300"/> <img src="https://user-images.githubusercontent.com/80665546/136636096-6ce5c801-2065-422b-93cc-90b5c8c5e94f.jpg" width="480" height="360"/>
