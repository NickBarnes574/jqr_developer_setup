# Managing Git Credentials

## Overview

This guide provides instructions for managing Git credentials on your local machine. It covers two primary areas: ignoring SSL certificate verification for Git operations and storing Git credentials to streamline your workflow. This approach simplifies interactions with repositories by reducing the need for repetitive authentication but should be used with an understanding of the associated security implications.

## Prerequisites

- Git installed on your local machine
- Basic familiarity with terminal or command line interface
- Access to your R2D2 GitLab repository's URL

## Configuration Steps

### Ignore SSL Certificate Verification

Ignoring SSL certificate verification is not recommended for everyday use due to security risks. However, it can be temporarily useful in environments where you have a high degree of control over the network and the server's certificate, such as self-hosted repositories with self-signed certificates.

1. **Bash Users**: Add the following line to your `.bashrc` file:
   ```bash
   export GIT_SSL_NO_VERIFY=1
   ```
   
2. **Zsh Users**: Add the following line to your `.zshrc` file:
   ```bash
   export GIT_SSL_NO_VERIFY=1
   ```

### Storing Git Credentials

Storing your Git credentials allows Git to remember your username and password, reducing the need to enter them for every push, pull, or fetch operation.

> NOTE: It's important to be aware that the following command will store your username and password in a plain text file called `.git-credentials` in your home directory

1. **Global Configuration**: Execute the following command in your terminal to tell Git to store credentials:
   ```sh
   git config --global credential.helper store
   ```

2. **Perform a Git Operation**: Initiate any Git operation that requires authentication (e.g., `git push`). When prompted, enter your username and R2D2 access token. This information will be saved in a `.git-credentials` file in your home directory, allowing future operations to proceed without manual authentication.

## Security Considerations

- **SSL Verification**: Disabling SSL certificate verification can expose you to man-in-the-middle attacks. Use this configuration only in controlled environments and aim to resolve certificate issues as a long-term solution.
  
- **Credential Storage**: Storing credentials in plaintext is convenient but poses a security risk if your computer is accessed by others. Ensure your machine is secure and consider using more secure methods, such as SSH keys, for authentication in the future.
