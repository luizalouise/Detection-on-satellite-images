import os
import cv2
from PIL import Image
from PIL.ImageQt import ImageQt

from PyQt5 import QtGui



class Detection(object):

    def making_detection(self, filePath, model) :

        img = filePath

        head_tail = os.path.split(img)

        results = model(img)

        if not results.pandas().xyxy[0].empty:

            os.chdir(head_tail[0])

            image = cv2.imread(img)  # dopisane 1

            results = self.score_frame(results)

            frame = self.plot_boxes(results, image, model)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im_pred = Image.fromarray(frame)

            im = im_pred.convert("RGBA")
            data = im.tobytes("raw", "RGBA")
            qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGBA8888)
            pix_img = QtGui.QPixmap.fromImage(qim)


            return pix_img


        else:
            return None

    def score_frame(self, results):

        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        print("s")
        print(type(labels))
        print(type(cord))
        return labels, cord

    def class_to_label(self, x, model):
        classes = model.names

        if classes[int(x)] == 'ship':
            classes[int(x)] = 'statek'
        elif classes[int(x)] == 'car':
            classes[int(x)] = 'auto'
        elif classes[int(x)] == 'stadium':
            classes[int(x)] = 'stadion'
        elif classes[int(x)] == 'plane':
            classes[int(x)] = 'samolot'

        print("c")
        print(type(classes[int(x)]))

        return classes[int(x)]

    def plot_boxes(self, results, frame, model):

        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        colors = [(0, 0, 192), (255, 205, 0), (67, 173, 0), (0, 255, 255)]

        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)
                bgr = colors[int(labels[i])]
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                text = self.class_to_label(labels[i], model) + " " + str(round(row[4], 2))
                cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)

        print("p")
        print(type(frame))
        return frame
