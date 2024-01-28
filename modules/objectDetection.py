import cv2
import numpy as np

# Die Funktion ermöglicht die Objekterkennung in einem Bild oder von einer Webcam.
# Parameter:
# - image_path: Der Dateipfad zum Bild, das bearbeitet werden soll (Standardwert ist None für Webcam).
def object_detection(image_path=None):
    try:
        # Parameter-Validierung
        if image_path and not isinstance(image_path, str):
            raise TypeError("Der Bildpfad muss eine Zeichenkette (String) sein oder None für die Verwendung der Webcam.")

        # Laden der Klassenlabels aus der Datei 'coco.names'.
        with open("nn_model/coco.names", "r") as f:
            LABELS = f.read().strip().split("\n")

        # Laden des vortrainierten YOLOv3-Tiny-Modells.
        net = cv2.dnn.readNet('nn_model/yolov3-tiny.weights', 'nn_model/yolov3-tiny.cfg')

        # Wenn ein Bildpfad angegeben wurde, verwenden Sie dieses Bild.
        if image_path:
            image = cv2.imread(image_path)
            if image is None:
                # Wenn das Bild nicht geladen werden kann, gibt eine Fehlermeldung aus und beendet die Funktion.
                print("Bild konnte nicht geladen werden.")
                return
            process_frame(image, net, LABELS)
            cv2.imwrite(image_path, image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            # Starten der Webcam.
            cap = cv2.VideoCapture(0)  # 0 ist normalerweise die Standard-ID der eingebauten Webcam.
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

    except Exception as e:
        # Falls ein Fehler auftritt, gibt eine Fehlermeldung aus.
        print(f"Fehler bei der Objekterkennung: {e}")

# Die Funktion verarbeitet ein Einzelbild für die Objekterkennung.
# Parameter:
# - image: Das Bild, das bearbeitet werden soll.
# - net: Das vortrainierte YOLOv3-Tiny-Modell.
# - LABELS: Die geladenen Klassenlabels.
def process_frame(image, net, LABELS):
    try:
        # Extrahiert die Höhe und Breite des Bildes.
        height, width = image.shape[:2]

        # Erzeugt einen Blob aus dem Bild für das neuronale Netz.
        blob = cv2.dnn.blobFromImage(image, scalefactor=1.0/255, size=(320, 320), mean=[0,0,0], swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(net.getUnconnectedOutLayersNames())

        # Initialisiert Listen für Begrenzungsrahmen, Vertrauenswerte und Klassen-IDs.
        boxes, confidences, classIDs = [], [], []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # Überprüft, ob das Vertrauen für die erkannte Klasse größer als 0.3 ist.
                if confidence > 0.3:
                    #
