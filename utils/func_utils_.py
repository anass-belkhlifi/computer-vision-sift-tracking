import cv2
import numpy as np 

#=========================================
#1.Initialisation et sélection de l’objet
#=========================================

# Chargement de la vidéo
def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")
    ret, frame0 = cap.read()
    if not ret:
        raise IOError(f"Cannot read video frame from: {video_path}")
    return cap, frame0


# Sélection manuelle de la ROI
def select_roi(frame):
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")
    return roi


#=============================================
#2.Extraction des points SIFT de l’objet cible
#=============================================

def extract_sift_features(image_gray):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image_gray, None)
    return keypoints, descriptors


#=============================================
#III – Extraction SIFT sur les frames vidéo
#=============================================

def compute_frame_sift(cap):
    kp = []
    des = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        k, d = extract_sift_features(frame_gray)
        kp.append(k)
        des.append(d)
        
    return kp, des


#=============================================
#Appariement des descripteurs
#=============================================

def match_descriptors(des_obj, des_frame, ratio=0.75):
    if des_obj is None or des_frame is None:
        return []

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des_obj, des_frame, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good_matches.append(m)

    return good_matches


#=============================================
#Estimation de la transformation géométrique
#=============================================

def estimate_homography(kp_obj, kp_frame, matches):
    if len(matches) < 4:
        return None, None

    src_pts = np.float32(
        [kp_obj[m.queryIdx].pt for m in matches]
    ).reshape(-1, 1, 2)

    dst_pts = np.float32(
        [kp_frame[m.trainIdx].pt for m in matches]
    ).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    return H, mask


#============================
#4.Relocalisation de l'objet
#============================

def draw_tracked_object(frame, H, roi_box):
    frame_out = frame.copy()

    pts = np.array([
        [roi_box[0], roi_box[1]],
        [roi_box[0] + roi_box[2], roi_box[1]],
        [roi_box[0] + roi_box[2], roi_box[1] + roi_box[3]],
        [roi_box[0], roi_box[1] + roi_box[3]]
    ], dtype=np.float32).reshape(-1, 1, 2)

    dst = cv2.perspectiveTransform(pts, H)
    cv2.polylines(frame_out, [np.int32(dst)], True, (0, 255, 0), 3)

    return frame_out


#=========================================
#Boucle principale de suivi SIFT
#=========================================

def sift_tracking(video_path):
    cap, frame0 = load_video(video_path)
    roi = select_roi(frame0)
    roi_box = (roi[0], roi[1], roi[2], roi[3])

    frame0_gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    kp_obj, des_obj = extract_sift_features(frame0_gray)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp_frame, des_frame = extract_sift_features(frame_gray)

        matches = match_descriptors(des_obj, des_frame)

        if len(matches) >= 4:
            H, mask = estimate_homography(kp_obj, kp_frame, matches)
            if H is not None:
                frame_out = draw_tracked_object(frame, H, roi_box)
                cv2.imshow("Tracked Object", frame_out)
            else:
                cv2.imshow("Tracked Object", frame)
        else:
            cv2.imshow("Tracked Object", frame)

        if cv2.waitKey(30) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()
