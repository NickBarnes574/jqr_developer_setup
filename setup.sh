#! /bin/bash

# Setup C toolkit for Linux
chmod +x ./scripts/c_toolkit_setup.sh
./scripts/c_toolkit_setup.sh

# Install CAC credentials for Firefox and Google Chrome
chmod +x ./scripts/install_posix_cac.sh
sudo ./scripts/install_posix_cac.sh

# Verify everything was installed correctly
chmod +x ./scripts/run_version_check.sh
./scripts/run_version_check.sh
