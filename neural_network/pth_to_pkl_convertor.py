import torch
import pickle

pth_model_path = "cat_traits_model.pth"
model_data = torch.load(pth_model_path)

pkl_model_path = "cat_traits_model.pkl"
with open(pkl_model_path, "wb") as f:
    pickle.dump(model_data, f)

print(f"Model has been converted to {pkl_model_path}")
