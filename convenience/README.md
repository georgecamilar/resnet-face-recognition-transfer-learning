Steps:

Way 1 (More Efficient):
1. Transform FaceRecognitionNet to json format
2. Load into page with TfJs inserted into the script tag
3. Add to video element


Way 2 (Easy to implement)(Chosen):
1. Create page with video element
2. Request for each second a prediction and update a label
