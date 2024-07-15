# Password Manager Script

This script allows you to securely store, retrieve, list, and delete passwords using encryption. 

## Prerequisites

- Python 3
- `pip3` for installing Python packages
- `cryptography` library

## Installation

1. **Download the Script**:
   Save the `password_manager.py` script to your local machine.

2. **Install Python and Pip**:
   Ensure Python 3 and `pip3` are installed on your system.

3. **Install `cryptography` Library**:
   Use `pip` to install the `cryptography` library:

   ```bash
   pip install cryptography

## Configuration

To make it easier to use the password manager script, you can set up aliases and update your PATH. Follow these steps:

1. **Open your shell configuration file**:

   - For `zsh` (default on macOS), open `~/.zshrc`:
     ```bash
     nano ~/.zshrc
     
   - For `bash`, open `~/.bashrc`:
     ```bash
     nano ~/.bashrc

2. **Add the following configurations**:
   Copy and paste the following lines into your shell configuration file:

   ```bash
   # Pip config
   export PATH=$PATH:/usr/local/bin
   alias pip='pip3'
   alias py='python3'

   # Password manager
   alias password_manager='python3 /Users/CHANGEME/password_manager.py'

3. **Save and close the file**:
    - In 'nano, press 'CTRL + X', then 'Y', and 'Enter'.

4. **Reload the shell configuration**:
    - For 'zsh':
    ```bash
    source ~/.zshrc

    - For 'bash':
    ```bash
    source ~/.bashrc

## Usage 

1. **Generate and Store a Password**
   ```bash
   py password_manager generate "Password Title" "YourPassword"

2. **Retrieve a Stored Passoword**
   ```bash
   py password_manager retrieve "Password Title"

3. **List All Stored Passwords**
   ```bash
   py password_manager list

4. **Delete a Stored Password**
   ```bash
   py password_manager delete "Password Title"

## Example Commands

- To generate and store a password:
  ```bash
  py password_manager generate "Email Password" "mypassword123"

- To list all stored passwords:
  ```bash
  py password_manager retrieve "Email Password"

- To list all stored passwords:
  ```bash
  py password_manager list


## Notes

- The script uses a master password to encrypt and decrypt the stored passwords.

- Ensure you remember your master password, as you will need it to retrieve or delete stored passwords.

- The passwords are stored in a JSON file named passwords.json in the same directory as the gitscript. 