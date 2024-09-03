from ultralytics import YOLO
from PIL import Image


model = YOLO(".\\assaultcube_trained_model\\best.pt") # path to .pt model file

results = model("./test.png") # path to test image

# Show the results
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image