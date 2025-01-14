import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import ReduceLROnPlateau, CosineAnnealingLR
import torch.nn.functional as F

# Load data
data = pd.read_csv("../data/datasets/balanced_outputs/balanced_hybrid.csv")


# Enhanced preprocessing with categorical handling
def preprocess_data(data):
    # Separate categorical and numerical columns
    categorical_cols = ['Sexe', 'Logement', 'Zone', 'Ext', 'Obs']
    numerical_cols = [col for col in data.columns if col not in categorical_cols + ['Race']]

    # One-hot encode categorical variables
    X_cat = pd.get_dummies(data[categorical_cols])

    # Normalize numerical variables
    scaler = StandardScaler()
    X_num = pd.DataFrame(scaler.fit_transform(data[numerical_cols]), columns=numerical_cols)

    # Combine features
    X = pd.concat([X_num, X_cat], axis=1)

    # Encode target
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data['Race'])

    return X.values, y


# Improved model architecture with residual connections
class ImprovedCNNModel(nn.Module):
    def __init__(self, input_shape, num_classes):
        super(ImprovedCNNModel, self).__init__()

        # First conv block
        self.conv1 = nn.Conv1d(1, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(64)
        self.conv2 = nn.Conv1d(64, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(64)
        self.downsample1 = nn.Conv1d(1, 64, kernel_size=1)  # Add downsampling layer

        # Second conv block
        self.conv3 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(128)
        self.conv4 = nn.Conv1d(128, 128, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm1d(128)
        self.downsample2 = nn.Conv1d(64, 128, kernel_size=1)  # Add downsampling layer

        # Third conv block
        self.conv5 = nn.Conv1d(128, 256, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm1d(256)

        # Global pooling
        self.adaptive_pool = nn.AdaptiveAvgPool1d(1)

        # Fully connected layers
        self.fc1 = nn.Linear(256, 512)
        self.bn_fc1 = nn.BatchNorm1d(512)
        self.fc2 = nn.Linear(512, 256)
        self.bn_fc2 = nn.BatchNorm1d(256)
        self.fc3 = nn.Linear(256, num_classes)

        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        # First residual block
        identity = self.downsample1(x)  # Downsample identity to match dimensions
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += identity
        x = F.relu(x)
        x = self.dropout(x)

        # Second residual block
        identity = self.downsample2(x)  # Downsample identity to match dimensions
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.bn4(self.conv4(x))
        x += identity
        x = F.relu(x)
        x = self.dropout(x)

        # Third conv block
        x = F.relu(self.bn5(self.conv5(x)))
        x = self.dropout(x)

        # Global pooling
        x = self.adaptive_pool(x)
        x = x.view(x.size(0), -1)

        # Fully connected layers
        x = F.relu(self.bn_fc1(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.bn_fc2(self.fc2(x)))
        x = self.dropout(x)
        x = self.fc3(x)

        return x


# K-fold Cross Validation training function
def train_with_kfold(X, y, k=5, epochs=500):
    kfold = KFold(n_splits=k, shuffle=True, random_state=42)
    fold_results = []

    for fold, (train_ids, val_ids) in enumerate(kfold.split(X)):
        print(f'\nFold {fold + 1}/{k}')

        # Prepare data for this fold
        X_train_fold = torch.from_numpy(X[train_ids]).float().unsqueeze(1)
        y_train_fold = torch.from_numpy(y[train_ids]).long()
        X_val_fold = torch.from_numpy(X[val_ids]).float().unsqueeze(1)
        y_val_fold = torch.from_numpy(y[val_ids]).long()

        train_data = TensorDataset(X_train_fold, y_train_fold)
        val_data = TensorDataset(X_val_fold, y_val_fold)
        train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_data, batch_size=32)

        # Initialize model and training components
        model = ImprovedCNNModel(input_shape=(X.shape[1],), num_classes=len(np.unique(y)))
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
        scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=10, verbose=True)

        # Train the model
        fold_result = train_model(model, train_loader, val_loader, criterion, optimizer, scheduler, epochs)
        fold_results.append(fold_result)

    return fold_results


def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()

    return correct / total

# Enhanced training loop with gradient clipping
def train_model(model, train_loader, test_loader, criterion, optimizer, scheduler, epochs=500):
    train_loss, train_accuracy = [], []
    best_test_accuracy = 0.0
    best_epoch = 0
    patience = 20
    patience_counter = 0

    for epoch in range(epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for data, target in train_loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()

        epoch_loss = running_loss / len(train_loader)
        epoch_acc = correct / total
        train_loss.append(epoch_loss)
        train_accuracy.append(epoch_acc)

        # Evaluation phase
        current_test_accuracy = evaluate_model(model, test_loader)

        # Learning rate scheduling
        scheduler.step(current_test_accuracy)

        # Early stopping with patience
        if current_test_accuracy > best_test_accuracy:
            best_test_accuracy = current_test_accuracy
            best_epoch = epoch + 1
            patience_counter = 0
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'test_accuracy': current_test_accuracy,
            }, "../project/best_cat_traits_model.pth")
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.4f}, "
                  f"Train Accuracy: {epoch_acc:.4f}, "
                  f"Test Accuracy: {current_test_accuracy:.4f} (Best Model Saved!)")
        else:
            patience_counter += 1
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.4f}, "
                  f"Train Accuracy: {epoch_acc:.4f}, "
                  f"Test Accuracy: {current_test_accuracy:.4f}")

        # Early stopping check
        if patience_counter >= patience:
            print(f"\nEarly stopping triggered after {patience} epochs without improvement")
            break

    print(f"\nTraining completed!")
    print(f"Best Test Accuracy: {best_test_accuracy:.4f} (achieved at epoch {best_epoch})")

    # Load and evaluate the best model
    checkpoint = torch.load("../project/best_cat_traits_model.pth")
    model.load_state_dict(checkpoint['model_state_dict'])
    final_test_accuracy = evaluate_model(model, test_loader)
    print(f"Final Test Accuracy (using best model): {final_test_accuracy:.4f}")

    return train_loss, train_accuracy, best_test_accuracy


# Main execution
if __name__ == "__main__":
    # Preprocess data
    X, y = preprocess_data(data)

    # Either use K-fold cross validation
    fold_results = train_with_kfold(X, y, k=5, epochs=500)

    # Or traditional train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Convert to PyTorch tensors
    X_train = torch.from_numpy(X_train).float().unsqueeze(1)
    X_test = torch.from_numpy(X_test).float().unsqueeze(1)
    y_train = torch.from_numpy(y_train).long()
    y_test = torch.from_numpy(y_test).long()

    # Create data loaders
    train_data = TensorDataset(X_train, y_train)
    test_data = TensorDataset(X_test, y_test)
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

    # Initialize model and training components
    model = ImprovedCNNModel(input_shape=(X_train.shape[2],), num_classes=len(np.unique(y)))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=10, verbose=True)

    # Train the model
    train_loss, train_accuracy, best_test_accuracy = train_model(
        model, train_loader, test_loader, criterion, optimizer, scheduler, epochs=1000
    )

    # Plot training history
    plt.figure(figsize=(10, 6))
    plt.plot(train_accuracy, label='Train Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Model Accuracy Over Time')
    plt.grid(True)
    plt.show()