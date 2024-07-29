
from clarifai.client.model import Model

# Your PAT (Personal Access Token) can be found in the Account's Security section
prompt = "Write me a bubble sort."
# You can set the model using model URL or model ID.
model_url="https://clarifai.com/meta/Llama-2/models/codellama-13b-instruct"


# Model Predict
model_prediction = Model(url=model_url,pat="f4ad2d6e9cb948598e9fa38fc341b240").predict_by_bytes(prompt.encode(), input_type="text")

print(model_prediction.outputs[0].data.text.raw)
