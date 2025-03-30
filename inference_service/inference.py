import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import os

# Detectar si hay GPU disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando: {device}")

# Ruta del modelo (ajustar si es necesario)
MODEL_PATH = "model/image_binary_classifierV3.pth"

# Definir la clase del modelo
class ImageBinaryClassifier(nn.Module):
    def __init__(self):
        super(ImageBinaryClassifier, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, kernel_size=9, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(256, 512, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        # Calcular automáticamente el tamaño de entrada para fc1
        self.fc1_input_dim = self._get_fc1_input_dim()
        self.fc1 = nn.Linear(self.fc1_input_dim, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 2)

        self.dropout = nn.Dropout(0.5)
        self.log_softmax = nn.LogSoftmax(dim=1)

    def _get_fc1_input_dim(self):
        """ Calcula dinámicamente el tamaño de entrada de fc1. """
        with torch.no_grad():
            dummy_input = torch.zeros(1, 3, 512, 512)  # Imagen de prueba (ajustar tamaño si es necesario)
            x = self.pool(F.relu(self.conv1(dummy_input)))
            x = self.pool(F.relu(self.conv2(x)))
            x = self.pool(F.relu(self.conv3(x)))
            x = self.pool(F.relu(self.conv4(x)))
            x = self.pool(F.relu(self.conv5(x)))
            return x.view(1, -1).shape[1]

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        x = self.pool(F.relu(self.conv5(x)))

        print("Shape antes de Flatten:", x.shape)  # Verificar tamaño antes de fc1

        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.log_softmax(self.fc3(x))

        return x


# Cargar el modelo
model = ImageBinaryClassifier().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# Transformaciones para preprocesar imágenes
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
])

def predict(image_path):
    """ Realiza una predicción sobre una imagen. """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"La imagen '{image_path}' no existe.")

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        prediction = torch.argmax(output, dim=1).item()

    return "Relevante" if prediction == 1 else "Irrelevante"

