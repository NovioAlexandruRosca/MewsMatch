import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

data = pd.read_excel("../data/datasets/balanced_outputs/balanced_hybrid.xlsx")


columns_to_keep = [
    "Sexe",
    "Age",
    "Nombre",
    "Logement",
    "Zone",
    "Ext",
    "Obs",
    "Timide",
    "Calme",
    "Effraye",
    "Intelligent",
    "Vigilant",
    "Perseverant",
    "Affectueux",
    "Amical",
    "Solitaire",
    "Brutal",
    "Dominant",
    "Agressif",
    "Impulsif",
    "Previsible",
    "Distrait",
    "Abondance",
    "PredOiseau",
    "PredMamm",
]
data = data[columns_to_keep + ["Race"]]

X = data[columns_to_keep].values
y = data["Race"].values.reshape(-1, 1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
encoder = OneHotEncoder()
y = encoder.fit_transform(y).toarray()
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=10)

input_size = X_train.shape[1]
hidden_layers = 3
hidden_size = 100
output_size = y_train.shape[1]
learning_rate = 0.01

weights = []
biases = []

print(X_train.shape)


def weight_and_bias_initialization(activation_type):
    global weights, biases
    weights.clear()
    biases.clear()

    if activation_type:
        limit_input = np.sqrt(1.0 / input_size)
        weights.append(
            np.random.uniform(-limit_input, limit_input, (input_size, hidden_size))
        )
        biases.append(np.zeros((1, hidden_size)))

        for _ in range(hidden_layers - 1):
            limit_hidden = np.sqrt(1.0 / hidden_size)
            weights.append(
                np.random.uniform(
                    -limit_hidden, limit_hidden, (hidden_size, hidden_size)
                )
            )
            biases.append(np.zeros((1, hidden_size)))

        limit_output = np.sqrt(1.0 / hidden_size)
        weights.append(
            np.random.uniform(-limit_output, limit_output, (hidden_size, output_size))
        )
        biases.append(np.zeros((1, output_size)))

    else:
        limit_input = np.sqrt(2.0 / input_size)
        weights.append(np.random.randn(input_size, hidden_size) * limit_input)
        biases.append(np.zeros((1, hidden_size)))

        for _ in range(hidden_layers - 1):
            limit_hidden = np.sqrt(2.0 / hidden_size)
            weights.append(np.random.randn(hidden_size, hidden_size) * limit_hidden)
            biases.append(np.zeros((1, hidden_size)))

        limit_output = np.sqrt(2.0 / hidden_size)
        weights.append(np.random.randn(hidden_size, output_size) * limit_output)
        biases.append(np.zeros((1, output_size)))


def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return (x > 0).astype(float)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def forward_propagation(x, activation_type):
    activations = [x]
    for i in range(len(weights) - 1):
        z = np.dot(activations[-1], weights[i]) + biases[i]
        a = sigmoid(z) if activation_type else relu(z)
        activations.append(a)

    z_output = np.dot(activations[-1], weights[-1]) + biases[-1]
    a_output = softmax(z_output)
    activations.append(a_output)
    return activations


def cross_entropy_loss(predictions, targets):
    predictions = np.clip(predictions, 1e-12, 1.0 - 1e-12)
    return -np.mean(np.sum(targets * np.log(predictions), axis=1))


def backpropagation(activations, y, activation_type):
    global weights, biases
    layer_errors = [activations[-1] - y]

    for i in range(len(weights) - 2, -1, -1):
        if activation_type:
            error = sigmoid_derivative(activations[i + 1]) * np.dot(
                layer_errors[-1], weights[i + 1].T
            )
        else:
            error = relu_derivative(activations[i + 1]) * np.dot(
                layer_errors[-1], weights[i + 1].T
            )

        layer_errors.append(error)

    layer_errors.reverse()

    for i in range(len(weights)):
        gradient_w = np.dot(activations[i].T, layer_errors[i]) / y.shape[0]
        gradient_b = np.sum(layer_errors[i], axis=0, keepdims=True) / y.shape[0]
        weights[i] -= learning_rate * gradient_w
        biases[i] -= learning_rate * gradient_b


def train(x_train, y_train, x_val, y_val, epochs=100, batch_size=64, activation_type=1):
    global learning_rate
    weight_and_bias_initialization(activation_type)

    for epoch in range(epochs):
        x_train, y_train = shuffle(x_train, y_train)

        for i in range(0, x_train.shape[0], batch_size):
            x_batch = x_train[i : i + batch_size]
            y_batch = y_train[i : i + batch_size]

            activations = forward_propagation(x_batch, activation_type)
            backpropagation(activations, y_batch, activation_type)

        val_activations = forward_propagation(x_val, activation_type)
        val_loss = cross_entropy_loss(val_activations[-1], y_val)
        val_predictions = np.argmax(val_activations[-1], axis=1)
        val_labels = np.argmax(y_val, axis=1)
        val_accuracy = np.mean(val_predictions == val_labels)

        print(
            f"Epoch {epoch + 1}/{epochs}, Loss: {val_loss:.4f}, Accuracy: {val_accuracy:.4f}"
        )


train(X_train, y_train, X_val, y_val, epochs=1000, batch_size=10, activation_type=1)
