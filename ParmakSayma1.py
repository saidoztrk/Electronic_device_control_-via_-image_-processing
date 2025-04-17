import cv2
from ElizlemeModulu  import HandDetector

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

def main():
    """
    Ana fonksiyon: Kamerayı başlatır, el tespiti yapar ve açık parmak sayısını gösterir.
    """
    # El algılama sınıfını başlat
    detector = HandDetector(detection_confidence=0.75)
    
    # Kamerayı başlat
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()  # Kameradan görüntü oku
        if not success:  # Görüntü alınamazsa döngüden çık
            print("Failed to read frame from camera. Exiting...")
            break

        # Elleri tespit et ve landmark'ları al
        frame = detector.find_hands(frame, draw=False)  # Landmark'ları çizmeyin
        lm_list = detector.find_positions(frame)

        # Parmak sayısını hesapla
        finger_count = count_fingers(lm_list)

        # Ekrana parmak sayısını yazdır
        cv2.putText(frame, f"{finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        # Görüntüyü kullanıcıya göster
        cv2.imshow("Finger Counter", frame)

        # 'q' tuşuna basıldığında çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Kamerayı serbest bırak
    cv2.destroyAllWindows()  # Tüm pencereleri kapat
    
if __name__ == "__main__":
    main()  # Ana fonksiyonu çalıştır
