import pickle

# Function to transform data to be ready for the model
# inputnya csv
with open("models/pipeline.pk", "rb") as f:
    pipeline = pickle.load(f)

# load model architecture for the model
with open("models/gold_1week_architecture.pkl", "rb") as f:
    model = pickle.load(f)
    print(type(model))  # See the object type
    print(model.__class__.__name__)  # See the class name

# load weights for the model
with open("models/gold_1week_weights.pkl", "rb") as f:
    weights = pickle.load(f)
