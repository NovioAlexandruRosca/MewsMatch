import time

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler, OneHotEncoder

data = pd.read_excel("../data/datasets/balanced_outputs/balanced_hybrid.xlsx")


def one_hot_encode(y):
    unique_classes = np.unique(y)
    one_hot_encoded = np.zeros((len(y), len(unique_classes)))
    for i, value in enumerate(y):
        one_hot_encoded[i, unique_classes == value] = 1
    return one_hot_encoded

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

def compute_scaler(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return mean, std

def scale_data(X, mean, std):
    return (X - mean) / std

mean, std = compute_scaler(X)
print("Medie:", mean)
print("STD:", std)

X = scale_data(X, mean, std)

y = one_hot_encode(y)

def data_split(X, y, test_size=0.2, random_state=None):

    if random_state is not None:
        np.random.seed(random_state)

    # Convert test_size to train_size
    train_size = 1 - test_size

    # Get unique classes and their indices
    unique_classes, class_counts = np.unique(y.argmax(axis=1), return_counts=True)
    train_indices = []
    test_indices = []

    # Split each class proportionally
    for cls in unique_classes:
        # Get indices for current class
        cls_indices = np.where(y.argmax(axis=1) == cls)[0]
        np.random.shuffle(cls_indices)

        # Calculate split point
        split_idx = int(train_size * len(cls_indices))

        # Add indices to train and test sets
        train_indices.extend(cls_indices[:split_idx])
        test_indices.extend(cls_indices[split_idx:])

    # Shuffle the indices
    np.random.shuffle(train_indices)
    np.random.shuffle(test_indices)

    # Return split datasets
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]


X_train, X_val, y_train, y_val = data_split(X, y, test_size=0.2)


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


def plot_history(training_history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    ax1.plot(training_history["train_loss"], label="Train Loss")
    ax1.plot(training_history["val_loss"], label="Validation Loss")
    ax1.set_title("Loss History")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.legend()

    ax2.plot(training_history["train_acc"], label="Train Accuracy")
    ax2.plot(training_history["val_acc"], label="Validation Accuracy")
    ax2.set_title("Accuracy History")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.legend()

    plt.tight_layout()
    plt.show()


def predictions_visualizer(
    x_val,
    y_val,
    num_samples,
    activation_type=1,
    dropout_rate=0.3,
    apply_dropout_flag=False,
):
    indices = np.random.choice(len(x_val), num_samples, replace=False)
    samples = x_val[indices]
    true_labels = np.argmax(y_val[indices], axis=1)

    activations = forward_propagation(
        samples,
        activation_type,
        # dropout_rate=dropout_rate,
        # apply_dropout_flag=apply_dropout_flag,
    )
    predicted_labels = np.argmax(activations[-1], axis=1)

    print("\nSample Predictions:")
    print("True Label | Predicted Label | Correct?")
    print("-" * 40)

    for i, (true_label, pred_label) in enumerate(zip(true_labels, predicted_labels)):
        correct = "✓" if true_label == pred_label else "✗"
        print(f"{true_label:^10} | {pred_label:^14} | {correct:^8}")

        if true_label != pred_label:
            print(f"Misclassified sample index: {indices[i]}")

    accuracy = np.mean(true_labels == predicted_labels)
    print(f"\nAccuracy on these {num_samples} samples: {accuracy:.4f}")


def train(x_train, y_train, x_val, y_val, epochs_wh_improvement=10, decay_factor=0.5, epochs=100, batch_size=64, activation_type=1):
    global learning_rate
    weight_and_bias_initialization(activation_type)

    accuracy_met = True
    best_val_loss = float("inf")
    epochs_since_improvement = 0
    start_time = time.time()

    training_history = {
        "train_loss": [],
        "val_loss": [],
        "train_acc": [],
        "val_acc": [],
    }

    for epoch in range(epochs):
        x_train, y_train = shuffle(x_train, y_train)
        train_predictions = []
        train_labels = []
        batch_losses = []

        for i in range(0, x_train.shape[0], batch_size):
            x_batch = x_train[i: i + batch_size]
            y_batch = y_train[i: i + batch_size]

            activations = forward_propagation(x_batch, activation_type)
            backpropagation(activations, y_batch, activation_type)

            batch_loss = cross_entropy_loss(activations[-1], y_batch)
            batch_losses.append(batch_loss)

            batch_predictions = np.argmax(activations[-1], axis=1)
            batch_labels = np.argmax(y_batch, axis=1)
            train_predictions.extend(batch_predictions)
            train_labels.extend(batch_labels)

        train_loss = np.mean(batch_losses)
        train_accuracy = np.mean(np.array(train_predictions) == np.array(train_labels))

        val_activations = forward_propagation(x_val, activation_type)
        val_loss = cross_entropy_loss(val_activations[-1], y_val)
        val_predictions = np.argmax(val_activations[-1], axis=1)
        val_labels = np.argmax(y_val, axis=1)
        val_accuracy = np.mean(val_predictions == val_labels)

        training_history["train_loss"].append(train_loss)
        training_history["val_loss"].append(val_loss)
        training_history["train_acc"].append(train_accuracy)
        training_history["val_acc"].append(val_accuracy)

        print(
            f"Epoch {epoch + 1}/{epochs}, "
            f"LR: {learning_rate}, "
            f"Loss: {val_loss:.4f}, "
            f"Train Acc: {train_accuracy:.4f}, "
            f"Val Acc: {val_accuracy:.4f}"
        )

        # if val_loss < best_val_loss:
        #     best_val_loss = val_loss
        #     epochs_since_improvement = 0
        # else:
        #     epochs_since_improvement += 1
        #
        # if epochs_since_improvement >= epochs_wh_improvement:
        #     learning_rate *= decay_factor
        #     print(f"Learning rate decay: {learning_rate:.6f}")
        #     epochs_since_improvement = 0
        #
        # if learning_rate < 0.000001:
        #     break
        #
        # if train_accuracy > 0.75 and accuracy_met:
        #     accuracy_met = False
        #     print(
        #         f"Accuracy of at least 75% was achieved after: {time.time() - start_time:.2f} seconds"
        #     )

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Training time: {total_time:.2f} seconds")
    plot_history(training_history)
    predictions_visualizer(
        x_val,
        y_val,
        num_samples=100,
        activation_type=1,
        dropout_rate=0.3,
        apply_dropout_flag=False,)


train(X_train, y_train, X_val, y_val, epochs_wh_improvement=15, decay_factor=0.2, epochs=1000, batch_size=10, activation_type=1)
