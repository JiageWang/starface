from utils.align import get_aligned_faces
from utils.utils import resize_min300
from arcface.arcface import Arcface
from mtcnn.mtcnn import MTCNN


class FaceModel(object):
    def __init__(self):
        self.mtcnn = MTCNN()
        self.arcface = Arcface()
        self.threshold = 0.8
        self.facebank = None
        self.ids = None

    def __call__(self, img):
        img = resize_min300(img)
        landmarks, bboxs = self.mtcnn(img)
        faces = get_aligned_faces(img, bboxs, landmarks)
        embeddings = []
        for face in faces:
            embedding = self.arcface(face)
            embeddings.append(embedding)
        return landmarks, bboxs, faces, embeddings

