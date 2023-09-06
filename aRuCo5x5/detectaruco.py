import cv2
import cv2.aruco as aruco

def detect_and_get_aruco_id(image_path):
    # Ler a imagem
    # Get an image 
    frame = cv2.imread(image_path)

    # Configurar o dicionário ArUco que você está usando (neste exemplo, usamos o 5x5)
    # Configuring the ArUco dictinary you are using (in this case, we are using the 5x5 version)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()

    # Detectar os marcadores na imagem
    # Detecting ther markers on the image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    detected_ids = []
    
    # Se algum marcador for detectado, adicione os IDs à lista detected_ids
    # Case some marker is detected, add the IDs to "detected-id" array
    if ids is not None:
        for i in ids:
            detected_ids.append(i[0])

    return detected_ids

# Detectar o ID do ArUco na imagem fornecida
# Detection the ArUco's ID into the obtained image
image_path = "/home/leandro/BrSw-IMAV2023/aRuCo5x5/arucoid900.png"
detected_ids = detect_and_get_aruco_id(image_path)
print(detected_ids)
