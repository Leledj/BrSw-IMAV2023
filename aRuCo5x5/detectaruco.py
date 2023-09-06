import cv2
import cv2.aruco as aruco

def detect_and_get_aruco_id(image_path):
    # Ler a imagem
    frame = cv2.imread(image_path)

    # Configurar o dicionário ArUco que você está usando (neste exemplo, usamos o 5x5)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()

    # Detectar os marcadores na imagem
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    detected_ids = []
    
    # Se algum marcador for detectado, adicione os IDs à lista detected_ids
    if ids is not None:
        for i in ids:
            detected_ids.append(i[0])

    return detected_ids

# Detectar o ID do ArUco na imagem fornecida
image_path = "/home/leandro/BrSw-IMAV2023/aRuCo5x5/arucoid900.png"
detected_ids = detect_and_get_aruco_id(image_path)
print(detected_ids)
