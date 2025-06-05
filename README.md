# GitHub Updater

This project is a software updater built using PyQt6 that checks for updates on GitHub and allows users to download and install the latest version of the application.

## Features

- Check for updates from a GitHub repository.
- Download the latest version of the software.
- Install updates seamlessly.
- User-friendly interface built with PyQt6.

## Project Structure

```
github-updater
├── src
│   ├── main.py               # Entry point of the application
│   ├── updater.py            # Contains the Updater class for managing updates
│   ├── ui
│   │   ├── main_window.py    # Main window UI class
│   │   └── updater_dialog.py  # Dialog for showing update progress
│   ├── utils
│   │   ├── github_api.py     # Functions for interacting with GitHub API
│   │   └── version.py        # Version class for version management
├── requirements.txt          # Required Python libraries
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/github-updater.git
   ```
2. Navigate to the project directory:
   ```
   cd github-updater
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application using the following command:
```
python src/main.py
```

Once the application is running, you can check for updates by clicking the "Check for Updates" button in the main window. If an update is available, you will be prompted to download and install it.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.