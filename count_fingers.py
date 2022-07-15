import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands  #Detectar los 21 puntos de referencia
mp_drawing = mp.solutions.drawing_utils  #Dibujar la conexión entre los puntos

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

state = None

# Definir una función para contar dedos
def countFingers(image, hand_landmarks, handNo=0):

    global state

    if hand_landmarks :
        landmarks = hand_landmarks[handNo].landmark
        # print(landmarks)
        fingers = []
        for index in tipIds:
            finger_tip_y = landmarks[index].y
            finger_bottom_y = landmarks[index-2].y

            thumb_tip_x = landmarks[index].x
            thumb_bottom_x = landmarks[index-2].x

            if index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    # print("El dedo con id ",index," está abierto")

                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    # print("El dedo con id ",index," está cerrado")

            else:
                if thumb_tip_x > thumb_bottom_x:
                    fingers.append(1)
                    # print("El pulgar está abierto")

                if thumb_tip_x < thumb_bottom_x:
                    fingers.append(0)
                    # print("El pulgar está cerrado")

        total_fingers = fingers.count(1)
        if total_fingers == 5:
            state = "Play"
        if total_fingers == 0 and state=="Play":
            state = "Pause"
            keyboard.press(Key.space)
        finger_tip_x = (landmarks[8].x)*width
        if total_fingers == 1:
            if finger_tip_x < width-400:
                keyboard.press(Key.left)
                print("Regresar")
            if finger_tip_x > width-40:
                keyboard.press(Key.right)
                print("Adelantar")
        

        text = f"Fingers:{total_fingers}"
        cv2.putText(image,text,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)


    # < >

    ####################################################

# Definir una función para
def drawHandLanmarks(image, hand_landmarks):

    # Dibujar conexiones entre los puntos de referencia
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detectar los puntos de referencia de las manos
    results = hands.process(image)

    # Obtener la posición de los puntos de referencia del resultado procesado
    hand_landmarks = results.multi_hand_landmarks

    # Dibujar puntos de referencia
    drawHandLanmarks(image, hand_landmarks)

    # Obtener la posición de los dedos de la mano
    ##################
    countFingers(image,hand_landmarks)
    ##################

    cv2.imshow("Controlador de medios", image)

    # Cerrar la ventana al presionar la barra espaciadora
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
