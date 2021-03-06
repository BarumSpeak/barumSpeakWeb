import cv2 as cv
import dlib
import numpy as np
import os
from module.compare.frame_number import f_num

def landmark(input_vid):
    # 얼굴 검출을 위해 디폴트 얼굴 검출기 사용
    detector = dlib.get_frontal_face_detector()
    # 검출된 얼굴에서 눈, 코, 입같은 랜드마크를 찾기 위해 사용할 학습모델을 로드합니다.
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # 웹캠으로부터 영상을 가져와 입력으로 사용합니다.
    cap = cv.VideoCapture(input_vid)

    MOUTH = list(range(48, 68))

    index = MOUTH

    icurrentframe = 0

    fps = cap.get(cv.CAP_PROP_FPS)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter('/home/ivpl-d04/Web/static/video/output.mp4', fourcc, fps, (width, height))

    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    
    on = int(f_num(input_vid))

    # 웹캠으로부터 입력을 받으려면 무한 반복을 해줘야함
    while icurrentframe < on:

        icurrentframe += 1

        ret, frame = cap.read()

        # 웹캠으로부터 이미지를 가져와서 그레이스케일로 변환한다.
        img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # 주어진 이미지에서 얼굴을 검출. 두번째 아규먼트는 업샘플링 횟수.
        dets = detector(img_gray, 1)

        for face in dets:

            # 주어진 이미지 img_frame의 검출된 얼굴 영역 face에서 랜드마크를 검출.
            shape = predictor(frame, face)  # 얼굴에서 68개 점 찾기

            list_points = []
            for p in shape.parts():
                list_points.append([p.x, p.y])

            list_points = np.array(list_points)

            # 검출된 랜드마크 중 index 변수에 지정된 부위만 이미지에 원으로 그려줌.
            for i, pt in enumerate(list_points[index]):
                pt_pos = (pt[0], pt[1])

                cv.circle(frame, pt_pos, 2, (0, 255, 0), -1)

            out.write(frame)

        # 결과 이미지를 화면에 보여주고 키보드 입력을 받음
        #cv.imshow('result', frame)    
    
    cap.release()

