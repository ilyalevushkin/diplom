from sklearn.svm import SVC

class ClassificationParams:
    def __init__(self):
        self.model = SVC(kernel='rbf', C=1e5)
