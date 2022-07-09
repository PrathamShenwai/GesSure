import cv2 as cv
import numpy as np
import mediapipe as mp
import tensorflow as tf
import pyautogui as py
import ctypes
import json
import joblib
import cv2
import numpy as np
from PIL import Image
from face_recognition import preprocessing
from PIL import ImageDraw, ImageFont


class verify_face:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    MODEL_PATH = 'model/face_recogniser.pkl'
    
    
    def draw_bb_on_img(self,faces, img):
        draw = ImageDraw.Draw(img)
        fs = max(20, round(img.size[0] * img.size[1] * 0.000005))
        font = ImageFont.truetype('fonts/font.ttf', fs)
        margin = 5

        for face in faces:
            if face.top_prediction.confidence * 100 > 0:
                text = '%s %.2f%%' % (face.top_prediction.label.upper(),
                                    face.top_prediction.confidence * 100)
                text_size = font.getsize(text)
                draw.rectangle(((int(face.bb.left), int(face.bb.top)),
                            (int(face.bb.right), int(face.bb.bottom))),
                            outline='green', width=2)
                draw.rectangle(((int(face.bb.left - margin),
                            (int(face.bb.bottom) + margin)),
                            (int(face.bb.left + text_size[0] + margin),
                            int(face.bb.bottom) + text_size[1] + 3
                            * margin)), fill='black')
                draw.text((int(face.bb.left), int(face.bb.bottom) + 2
                        * margin), text, font=font)


    def mediapipe_detection(self,image, hands):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        return image, results


    def draw_landmarks(self,image, results):
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS,
                                        self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                        )
            return image


    def extract_landmark_coordinates_array(self,results, flatten=True):
        if results.multi_hand_landmarks:
            hand_keypoints = np.array([[res.x, res.y, res.z] for res in
                                    results.multi_hand_landmarks[0].landmark]).flatten()
            return hand_keypoints
        else:
            return np.zeros(63)  # 21 * 3 which is the x,y,z of the 21 landmarks


    def execute_interface(self,res, sequence, actions):
        if actions[np.argmax(res)] == 'gesture 1':
            py.hotkey('ctrl', 's')

        elif actions[np.argmax(res)] == 'gesture 2':
            py.hotkey('alt', 'F4')

        elif actions[np.argmax(res)] == 'gesture 3':
            py.hotkey('ctrl', 'p')

        elif actions[np.argmax(res)] == 'gesture 4':
            ctypes.windll.user32.LockWorkStation()

        elif actions[np.argmax(res)] == 'gesture 5':
            py.hotkey('win', 'D')
            py.hotkey('alt', 'F4')
            py.press('down')
            py.press('enter')

        else:
            py.hotkey('Idle')


    def capture(self):
        model = tf.keras.models.load_model('../final_weights_4.h5')
        face_recogniser = joblib.load(self.MODEL_PATH)
        preprocess = preprocessing.ExifOrientationNormalize()
        sequence = []
        max_gesture = []
        threshold = 0.6
        
        actions = np.array(['gesture 1', 'gesture 2', 'gesture 3', 'gesture 4', 'gesture 5', 'random'])

        cap = cv.VideoCapture(0)

        skip = 0

        with self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
            while cap.isOpened():

                ret, frame = cap.read()
                frame = cv.flip(frame, 1)
                img = Image.fromarray(frame)
                image, results = self.mediapipe_detection(frame, hands)
                faces = face_recogniser(preprocess(img))
                if faces is not None:
                    self.draw_bb_on_img(faces, img)
                # Make detections
                with open('data.json','r') as f:
                    pred=json.load(f)
                m = max(set(pred),key=pred.count)
                if m=='1':
                    self.draw_landmarks(image, results)

                    # 2. Prediction logic
                    if not results.multi_hand_landmarks:
                        cv.putText(image, 'No hands', (0, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
                        if max_gesture:
                            print("The max gesture is : ", max(set(max_gesture), key=max_gesture.count))
                            self.execute_interface(res, sequence, actions)
                        sequence = []
                        max_gesture = []
                    else:
                        keypoints = self.extract_landmark_coordinates_array(results)
                        sequence.append(keypoints)
                        sequence = sequence[-20:]
                        if len(sequence) == 20:
                            res = model.predict(np.expand_dims(sequence, axis=0))[0]
                            if res[np.argmax(res)] > threshold:
                                cv.putText(image, ' '.join(actions[np.argmax(res)]), (0, 40),
                                        cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
                                print("the action is : {action_name} with probability : {prob}".format(
                                    action_name=actions[np.argmax(res)], prob=np.amax(res)))
                                max_gesture.append(actions[np.argmax(res)])
                            else:
                                cv.putText(image, ' '.join(actions[5]), (0, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                        cv.LINE_AA)

                cv.imshow('OpenCV Feed', image)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv.destroyAllWindows()


    def verify(self):
        self.capture()


if __name__ == '__main__':
    verify_face().verify()
