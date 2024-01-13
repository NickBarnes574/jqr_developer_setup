#! /bin/bash

# Setup C toolkit for Linux
chmod +x ./scripts/c_toolkit_setup.sh
./scripts/c_toolkit_setup.sh

# Verify everything was installed correctly
chmod +x ./scripts/run_version_check.sh
./scripts/run_version_check.sh

#----------Optional Configurations----------

# Setup Git
chmod +x ./scripts/git_config.sh
./scripts/git_config.sh

# Install CAC credentials for Firefox and Google Chrome
chmod +x ./scripts/install_posix_cac.sh
./scripts/install_posix_cac.sh

# Setup SSH keys
chmod +x ./scripts/ssh_key_setup.sh
./scripts/ssh_key_setup.sh
