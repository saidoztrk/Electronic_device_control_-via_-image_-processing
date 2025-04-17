# hand_detector.py
import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5, modelComplexity=1):
        """
        El algılama sınıfı. Mediapipe kullanarak elleri algılar ve landmark noktalarını döndürür.
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.modelComplex = modelComplexity
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.modelComplex, self.detection_confidence, self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """
        Görüntüdeki elleri bulur ve istenirse landmark noktalarını çizer.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Mediapipe için RGB formatına çevir
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return img

    def find_positions(self, img, hand_no=0):
        """
        Görüntüdeki belirli bir elin landmark pozisyonlarını döndürür.
        """
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # Piksel koordinatlarını hesapla
                lm_list.append((cx, cy))
        return lm_list

def count_fingers(landmarks):
    """
    Landmark noktalarına göre açık parmakların sayısını hesaplar.
    """
    if not landmarks:  # Eğer landmark listesi boşsa
        return 0

    fingers = []

    # Başparmak: Ucu (TIP) boğumdan (IP) sağdaysa açık
    if landmarks[4][0] > landmarks[3][0]:  # Yatay düzlemde kontrol
        fingers.append(1)  # Açık
    else:
        fingers.append(0)  # Kapalı

    # Diğer parmaklar: Uç (TIP) ile orta boğum (PIP) arasındaki dikey fark kontrol edilir
    FINGER_TIPS = [8, 12, 16, 20]  # Parmak uçlarının landmark indeksleri
    FINGER_PIPS = [6, 10, 14, 18]  # Parmak orta boğumlarının landmark indeksleri

    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        if landmarks[tip][1] < landmarks[pip][1]:  # Dikey düzlemde kontrol
            fingers.append(1)  # Açık
        else:
            fingers.append(0)  # Kapalı

    return sum(fingers)  # Açık parmakların toplamını döndür
