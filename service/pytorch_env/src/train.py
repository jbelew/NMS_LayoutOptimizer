import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
# Assuming data_generator.py is in the same directory
from data_generator import train_loader, num_output_classes, generate_training_data
from modules_refactored import modules
from modules_data import get_tech_modules_for_training # Import get_tech_modules_for_training from modules_data.py

# Set the tech filter here
tech_filter = "infra"

# Example usage:
num_samples = 32  # Adjust this to a larger number for better results
grid_width = 10
grid_height = 6
max_supercharged = 4
ship = "Exotic"
num_techs = len([tech_data["key"] for tech_data in modules[ship]["types"]["weapons"]])

X_train, y_train, bonus_scores, num_output_classes = generate_training_data(num_samples, grid_width, grid_height, max_supercharged, ship, num_techs, tech_filter)

# Create a custom dataset that includes bonus scores
class BonusDataset(data.Dataset):
    def __init__(self, X, y, bonus):
        self.X = X
        self.y = y
        self.bonus = bonus

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx], self.bonus[idx]

train_dataset = BonusDataset(X_train, y_train, bonus_scores)
train_loader = data.DataLoader(train_dataset, batch_size=32, shuffle=True)

class ModulePlacementCNN(nn.Module):
    def __init__(self, input_channels, num_output_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, 16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        # Calculate flattened size dynamically based on input size.  This is CRUCIAL.
        self._to_linear = None
        self.fc1_placement = nn.Linear(32 * 1 * 2, 128)  # Adjusted, but will be overwritten
        self.fc2_placement = nn.Linear(128, num_output_classes)
        self.fc1_bonus = nn.Linear(32 * 1 * 2, 128)  # Adjusted, but will be overwritten
        self.fc2_bonus = nn.Linear(128, 1)

    def forward(self, x):
        # x shape: [batch_size, input_channels, height, width]  e.g., [32, 1, 6, 10]
        #print(f"Initial input shape: {x.shape}")  # Debugging
        x = self.pool(self.relu(self.conv1(x)))
        # After conv1 and pool: [batch_size, 16, height/2, width/2] e.g., [32, 16, 3, 5]
        #print(f"After conv1 and pool: {x.shape}")  # Debugging
        x = self.pool(self.relu(self.conv2(x)))
        # After conv2 and pool: [batch_size, 32, height/4, width/4] e.g., [32, 32, 1, 2]
        #print(f"After conv2 and pool: {x.shape}")  # Debugging

        if self._to_linear is None:
            self._to_linear = x.size()[1] * x.size()[2] * x.size()[3]
            #print(f"Calculated _to_linear: {self._to_linear}") # Debugging
            self.fc1_placement = nn.Linear(self._to_linear, 128)
            self.fc1_bonus = nn.Linear(self._to_linear, 128)

        x = x.view(x.size(0), -1)  # Flatten
        # After flattening: [batch_size, flattened_size] e.g., [32, 64]
        #print(f"After flatten: {x.shape}")  # Debugging
        x_placement = self.relu(self.fc1_placement(x))
        x_placement = self.fc2_placement(x_placement)
        #print(f"Output placement shape: {x_placement.shape}") # Debugging
        x_bonus = self.relu(self.fc1_bonus(x))
        x_bonus = self.fc2_bonus(x_bonus)
        #print(f"Output bonus shape: {x_bonus.shape}") # Debugging
        return x_placement, x_bonus



# Hyperparameters
learning_rate = 0.001
num_epochs = 100
batch_size = 32

# Initialize model, loss function, and optimizer
model = ModulePlacementCNN(input_channels=1, num_output_classes=num_output_classes)
criterion_placement = nn.CrossEntropyLoss()
criterion_bonus = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Initialize TensorBoard writer (optional, but recommended)
writer = SummaryWriter()

# Training loop
for epoch in range(num_epochs):
    running_loss_placement = 0.0
    running_loss_bonus = 0.0
    for i, (inputs, targets, bonus_scores) in enumerate(train_loader):
        #print(f"Batch {i+1}, Input shape from data loader: {inputs.shape}") # Debugging
        #inputs = inputs.view(-1, 1, 6, 10)  # Ensure correct input shape [32, 1, 6, 10]
        #print(f"Batch {i+1}, Reshaped input shape: {inputs.shape}") # Debugging

        #print(f"Batch {i+1}, Target shape from data loader: {targets.shape}") # Debugging
        # targets shape: [batch_size, grid_height, grid_width] e.g., [32, 6, 10]

        # Reshape targets for CrossEntropyLoss
        targets = targets.view(-1)  # Flatten the target grid
        #print(f"Batch {i+1}, Reshaped target shape: {targets.shape}")

        bonus_scores = bonus_scores.view(-1, 1).float()
        #print(f"Batch {i+1}, Bonus scores shape: {bonus_scores.shape}") # Debugging

        optimizer.zero_grad()
        outputs_placement, outputs_bonus = model(inputs)
        # outputs_placement shape: [batch_size, num_output_classes] e.g., [32, 5]
        #print(f"Batch {i+1}, Output placement shape: {outputs_placement.shape}") # Debugging

        loss_placement = criterion_placement(outputs_placement, targets)
        loss_bonus = criterion_bonus(outputs_bonus, bonus_scores)
        loss = loss_placement + loss_bonus  # Combine losses
        loss.backward()
        optimizer.step()

        running_loss_placement += loss_placement.item()
        running_loss_bonus += loss_bonus.item()

        if i % 100 == 99:
            print(
                f"[{epoch + 1}, {i + 1:5d}] loss_placement: {running_loss_placement / 100:.3f} loss_bonus: {running_loss_bonus / 100:.3f}"
            )
            writer.add_scalar("Loss/train_placement", running_loss_placement / 100, epoch * len(train_loader) + i)
            writer.add_scalar("Loss/train_bonus", running_loss_bonus / 100, epoch * len(train_loader) + i)
            running_loss_placement = 0.0
            running_loss_bonus = 0.0

print("Finished Training")
writer.close()

# Save the trained model (optional)
torch.save(model.state_dict(), "module_placement_model.pth")
