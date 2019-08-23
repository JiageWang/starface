import os

import cv2
import pickle
import numpy as np
from tqdm import tqdm

from face_model import FaceModel

face_model = FaceModel()


def get_facebank(path):
    names = []
    embeddings = []
    folders = os.listdir(path)
    with open("starlist.txt", 'w', encoding='utf-8') as f:
        for name in tqdm(folders):
            file = os.path.join(path, name, name + '.jpg')
            starimg = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
            if starimg is None: continue
            _, _, starface, embedding = face_model(starimg)
            if len(embedding) != 1: continue
            f.write(name + '\n')
            names.append(name)
            embeddings.append(embedding[0])
    with open('facebank.pkl', 'wb') as f:
        pickle.dump((names, embeddings), f)
    return names, embeddings


if __name__ == "__main__":
    face_bank = get_facebank('starImages')
