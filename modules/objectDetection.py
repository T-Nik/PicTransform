# Objekterkennung

'''
Beschreibung der Funktion:
Mit dieser Funktion können Objekte in einem importierten Bild oder
in einem Live-Video von einer Webcam erkannt werden.
Parameter:
    - image_path (optional): Der Dateipfad zum Bild, auf dem die Objekterkennung durchgeführt
      werden soll. Wenn kein Pfad angegeben wird, wird die Webcam verwendet, um
      Live-Objekterkennung durchzuführen.
'''

import cv2
import numpy as np

def object_detection(image_path=None):
    # Klassenlabels laden
    with open("nn_model/coco.names", "r") as f:
        LABELS = f.read().strip().split("\n")

    # Laden des vortrainierten Modells
    net = cv2.dnn.readNet('nn_model/yolov3-tiny.weights', 'nn_model/yolov3-tiny.cfg')

    # Wenn ein Bildpfad angegeben wurde, verwenden Sie dieses Bild
    if image_path:
        image = cv2.imread(image_path)
        if image is None:
            print("Bild konnte nicht geladen werden.")
            return
        process_frame(image, net, LABELS)
        cv2.imwrite(image_path, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        # Starten der Webcam
        cap = cv2.VideoCapture(0)  # 0 ist normalerweise die Standard-ID der eingebauten Webcam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, image = cap.read()
            if not ret:
                break

            process_frame(image, net, LABELS)

            cv2.imshow("Live Object Detection", image)
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Live Object Detection", cv2.WND_PROP_VISIBLE) < 1:
                break

        cap.release()
        cv2.destroyAllWindows()

def process_frame(image, net, LABELS):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, scalefactor=1.0/255, size=(320, 320), mean=[0,0,0], swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(net.getUnconnectedOutLayersNames())

    boxes, confidences, classIDs = [], [], []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.3:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, box_width, box_height) = box.astype("int")

                x = int(centerX - (box_width / 2))
                y = int(centerY - (box_height / 2))

                boxes.append([x, y, int(box_width), int(box_height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.5)
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [0, 255, 0]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = LABELS[classIDs[i]] + " " + str( int(confidences[i] * 100)) + "%"
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Verwendung der Funktion
# object_detection() # Für die Verwendung der Kamera
# object_detection('path/to/image.jpg') # Für die Verwendung eines Bildes