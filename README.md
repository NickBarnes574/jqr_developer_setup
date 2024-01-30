# CSD-T JQR Developer Environment Setup Script for Ubuntu 22.04

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Getting Started](#getting-started)
   - [Download the Script](#1-download-the-script)
   - [Make the Script Executable](#2-make-the-script-executable)
   - [Run the Script](#3-run-the-script)
   - [Follow the Prompts](#4-follow-the-prompts)
   - [Monitor the Installation](#5-monitor-the-installation)
   - [Complete the Setup](#6-complete-the-setup)
   - [Version Checks](#7-version-checks)
5. [Packages and Extensions Installed](#packages-and-extensions-installed)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [OPTIONAL: Version Checks](#optional-version-checks)

## Overview

This script is designed to automate the setup of a developer environment on Ubuntu 22.04. It installs essential development tools, software packages, and Visual Studio Code (VS Code) extensions necessary for working on the CSD-T JQR project. The script is ideal for developers who want a quick and efficient way to set up their working environment on a new Ubuntu installation.

## Features

- Automated installation of essential development tools and libraries.
- Setup of Visual Studio Code with useful extensions for development.
- Optional configurations for Git, CAC credentials, and SSH keys.
- Easy-to-use and customizable for different development needs.

## Requirements

- Ubuntu 22.04 operating system.
- Internet connection for downloading packages and extensions.
- Sufficient permissions (ideally, run as a user with `sudo` privileges).

## Getting Started

### 1. Download the Script

Clone the repository or download the script files to your local machine. Ensure that the script (`run_setup.sh`) and its associated directories (`src`, `scripts`) are in the same directory.

### 2. Make the Script Executable

Before running the script, make sure it is executable:

```bash
chmod +x run_setup.sh
```

### 3. Run the Script

Execute the script:
>NOTE: Avoid running with sudo priveleges, as it can interfere with the setup process.
```bash
./run_setup.sh
```

### 4. Follow the Prompts

The script will display a list of software to be installed and ask for confirmation before proceeding. Press `y` to continue or `n` to exit.

![intro](/images/22.04_setup.png)

### 5. Monitor the Installation

Watch the installation process. The script will handle everything automatically, including updating the package lists, installing the packages, and setting up VS Code extensions.

### 6. Complete the Setup

After installation, the script may offer additional optional configurations such as setting up Git, POSIX CAC, SSH keys, and custom aliases. Follow the prompts to complete these setups if desired.

### 7. Version Checks

After all installations are completed, the system will run a version check to verify that all packages and extenions were installed correctly

![version_checks](/images/version_checks.gif)

## Packages and Extensions Installed

The script installs the following:

- **Development Tools**: build-essential, make, cmake, curl, etc.
- **Python Tools**: pip, pylint.
- **C/C++ Tools**: clang suite, cunit, valgrind, Address Sanitizer.
- **Static Analyzers**: cppcheck.
- **Window Manager**: i3 (a dynamic tiling window manager).
- **Version Control**: Git.
- **VS Code Extensions**: Extensions for C/C++, Python, Doxygen documentation, PDF viewing, and more.

## Customization

To customize the installations, modify the `base_install` function in the script. Add or remove calls to `install_package_if_not_present` and `install_extension_if_not_present` as needed.

## Troubleshooting

If you encounter errors:

- Ensure you have internet connectivity.
- Verify you have `sudo` privileges.
- Check if Ubuntu 22.04 is up-to-date.

For specific errors, refer to the console output. Most issues will be related to package availability or network problems.

> NOTE: If version checks fail, ensure that you are running the installation on 22.04 and not 20.04.

![fail](/images/fail.png)

## OPTIONAL: Version Checks
If desired, you can run version checks separately.
> **NOTE:** If you are running this script for the first time on a clean Ubuntu 22.04 install, all packages will display a `[FAIL] [NOT FOUND]` message

```bash
chmod +x run_version_check.sh

./run_version_check.sh
```