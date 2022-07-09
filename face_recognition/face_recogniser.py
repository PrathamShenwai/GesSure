from collections import namedtuple
import json
Prediction = namedtuple('Prediction', 'label confidence')
Face = namedtuple('Face', 'top_prediction bb all_predictions')
BoundingBox = namedtuple('BoundingBox', 'left top right bottom')
lst=[]

def top_prediction(idx_to_class, probs):
    print(probs)
    counter=0
    top_label = probs.argmax()
    if len(lst)<10:
    	lst.append(top_label)
    else:
    	lst[counter]=top_label
    	counter=counter+1
    	if counter==10:
    		counter=0
    with open("data.json","w") as f:
    	json.dump(str(lst),f)
   	
   
   
    return Prediction(label=idx_to_class[top_label], confidence=probs[top_label])


def to_predictions(idx_to_class, probs):
    return [Prediction(label=idx_to_class[i], confidence=prob) for i, prob in enumerate(probs)]


class FaceRecogniser:
    def __init__(self, feature_extractor, classifier, idx_to_class):
        self.feature_extractor = feature_extractor
        self.classifier = classifier
        self.idx_to_class = idx_to_class

    def recognise_faces(self, img):
        bbs, embeddings = self.feature_extractor(img)
        if bbs is None:
            # if no faces are detected
            return []

        predictions = self.classifier.predict_proba(embeddings)
	
	
	
        return [
            Face(
                top_prediction=top_prediction(self.idx_to_class, probs),
                bb=BoundingBox(left=bb[0], top=bb[1], right=bb[2], bottom=bb[3]),
                all_predictions=to_predictions(self.idx_to_class, probs)
            )
            for bb, probs in zip(bbs, predictions)
        ]

    def __call__(self, img):
        return self.recognise_faces(img)
