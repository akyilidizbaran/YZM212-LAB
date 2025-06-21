import os
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# 0) Ensure data/ folder exists
os.makedirs("data", exist_ok=True)

# 1) Download the gzipped CSV if not already present
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz"
LOCAL_PATH = "data/covtype.data.gz"
if not os.path.isfile(LOCAL_PATH):
    print("Downloading covtype.data.gz...", end=" ")
    urllib.request.urlretrieve(URL, LOCAL_PATH)
    print("done.")

# 2) Load into pandas (no header, gzip)
df = pd.read_csv(LOCAL_PATH, compression="gzip", header=None)

# 3) Split features & labels, enforce float64
X = df.iloc[:, :-1].values.astype(np.float64)
y_raw = df.iloc[:, -1].values.astype(np.int64)  # cover types 1–7

# 4) Map raw labels (1–7) to 0–6 and one-hot encode
classes = np.unique(y_raw)
y_idx = np.searchsorted(classes, y_raw)          # 0..6
Y = np.eye(len(classes), dtype=np.float64)[y_idx]

# 5) Train/test split
X_train, X_test, Y_train, Y_test, y_train, y_test = train_test_split(
    X, Y, y_idx, test_size=0.2, random_state=42, stratify=y_idx
)

# 6) Two‐layer NN with forward/backward
class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim, lr=0.01):
        np.random.seed(42)
        self.lr = float(lr)
        self.W1 = (np.random.randn(input_dim, hidden_dim) *
                   np.sqrt(2.0/input_dim)).astype(np.float64)
        self.b1 = np.zeros((1, hidden_dim), dtype=np.float64)
        self.W2 = (np.random.randn(hidden_dim, output_dim) *
                   np.sqrt(2.0/hidden_dim)).astype(np.float64)
        self.b2 = np.zeros((1, output_dim), dtype=np.float64)

    def relu(self, Z): return np.maximum(0, Z)
    def d_relu(self, Z): return (Z > 0).astype(np.float64)

    def softmax(self, Z):
        Z = Z.astype(np.float64)
        shift = Z - Z.max(axis=1, keepdims=True)
        expZ = np.exp(shift)
        return expZ / expZ.sum(axis=1, keepdims=True)

    def forward(self, X):
        self.Z1 = X.dot(self.W1) + self.b1
        self.A1 = self.relu(self.Z1)
        self.Z2 = self.A1.dot(self.W2) + self.b2
        self.A2 = self.softmax(self.Z2)
        return self.A2

    def backward(self, X, Y):
        m = X.shape[0]
        dZ2 = self.A2 - Y
        dW2 = self.A1.T.dot(dZ2) / m
        db2 = dZ2.sum(axis=0, keepdims=True) / m

        dA1 = dZ2.dot(self.W2.T)
        dZ1 = dA1 * self.d_relu(self.Z1)
        dW1 = X.T.dot(dZ1) / m
        db1 = dZ1.sum(axis=0, keepdims=True) / m

        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def train(self, X, Y, epochs=100):
        self.loss_history = []
        for epoch in range(1, epochs+1):
            Y_hat = self.forward(X)
            loss = -np.sum(Y * np.log(Y_hat + 1e-8)) / X.shape[0]
            self.loss_history.append(loss)
            self.backward(X, Y)
            if epoch % 10 == 0:
                print(f"Epoch {epoch}/{epochs} — Loss: {loss:.4f}")

# 7) Instantiate & train
nn = NeuralNetwork(input_dim=X_train.shape[1],
                   hidden_dim=64,
                   output_dim=Y_train.shape[1],
                   lr=0.05)
nn.train(X_train, Y_train, epochs=100)

# 8) Plot training loss
plt.figure(figsize=(6,4))
plt.plot(nn.loss_history)
plt.title("Epoch vs Cross-Entropy Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.tight_layout()
plt.show()

# 9) Evaluate on test set
y_pred = np.argmax(nn.forward(X_test), axis=1)
cm = pd.crosstab(pd.Series(y_test, name="Actual"),
                 pd.Series(y_pred, name="Predicted"))

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix (Forest Cover Types)")
plt.tight_layout()
plt.show()

print(f"Test Accuracy: {(y_pred == y_test).mean():.4f}")
