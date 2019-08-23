import cv2
import pickle
import numpy as np


from face_model import FaceModel
from utils.utils import compare_embedding

with open('facebank.pkl', 'rb') as f:
    names, face_bank = pickle.load(f)

face_model = FaceModel()


def find_similar_star(path, datapath='starImages'):
    myimg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)  # -1表示cv2.IMREAD_UNCHANGED
    _, _, myface, embedding = face_model(myimg)
    if len(myface) != 1:
        return None, None
    # 寻找最相似明星
    idx = compare_embedding(embedding[0], face_bank)
    starnname = names[idx]
    # 获取明星脸
    file = datapath + '\{}\{}.jpg'.format(starnname, starnname)
    starimg = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)  # -1表示cv2.IMREAD_UNCHANGED
    _, _, starface, _ = face_model(starimg)
    # 人脸对比
    myface = myface[0]
    starface = starface[0]
    h, w = starface.shape[:2]
    myface = cv2.resize(myface, (w, h))
    # myface = cv2.GaussianBlur(myface, ksize=(15,15), sigmaX=0)
    result = np.hstack((myface, starface))
    return starnname, result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", '-i', default='example/lx.jpg')
    args = parser.parse_args()

    star_name, compare_img = find_similar_star(args.img)
    if star_name is None:
        print('检测到多张人脸或未检测到人脸')
        exit(-1)
    print('与您最相似的明星为{}'.format(star_name))
    cv2.imshow('compare', compare_img)
    cv2.waitKey()
    cv2.destroyAllWindows()
