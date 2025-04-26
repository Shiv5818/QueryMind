import google.generativeai as genai
genai.configure(api_key="AIzaSyC4OGwYFG5EqF_aa9mOftE_KAhkh2wxPSE")
for model in genai.list_models():
    print(model.name)