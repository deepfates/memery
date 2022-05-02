import torch
import clip
from clip.model import CLIP
from tqdm import tqdm
from torch.utils.data import DataLoader
from torch import device
from torchvision.transforms import Compose

def load_model(device: device) -> CLIP:
    model, _ = clip.load("ViT-B/32", device, jit=False)
    model = model.float()
    return(model)

def image_encoder(img_loader: DataLoader, device: device, model: CLIP):
    image_embeddings = torch.tensor(()).to(device)
    with torch.no_grad():
        for images, labels in tqdm(img_loader):
            batch_features = model.encode_image(images.to(device))
            image_embeddings = torch.cat((image_embeddings, batch_features)).to(device)

    image_embeddings = image_embeddings / image_embeddings.norm(dim=-1, keepdim=True)
    return(image_embeddings)

def text_encoder(text: str, device: device, model: CLIP):
    with torch.no_grad():
        text = clip.tokenize(text).to(device)
        text_features = model.encode_text(text)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return(text_features)

def image_query_encoder(image, device: device, model: CLIP):
    with torch.no_grad():
        image_embed = model.encode_image(image.unsqueeze(0).to(device))
    image_embed = image_embed / image_embed.norm(dim=-1, keepdim=True)
    return(image_embed)