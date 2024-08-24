#!/bin/bash

# Step 1: Install Bazel

# Update and install prerequisites
sudo apt update
sudo apt install apt-transport-https curl gnupg -y

# Add Bazel’s Distribution URI as a package source
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings/

# Add the Bazel repository to your system’s package manager
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] \
https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

# Update the package list and install Bazel
sudo apt update
sudo apt install bazel -y

# Verify Bazel installation
bazel --version

# Step 2: Set Up Python Environment (Optional)

# Install Python and pip (if not already installed)
sudo apt install python3 python3-pip -y

# Install virtualenv
sudo pip3 install virtualenv

# Create a virtual environment (in the current directory)
virtualenv venv

# Activate the virtual environment
source venv/bin/activate

# Optionally, install necessary Python packages (uncomment and modify the following line)
# pip install <package_name>

echo "Bazel installation and Python environment setup complete."
echo "To deactivate the virtual environment, run 'deactivate'."
