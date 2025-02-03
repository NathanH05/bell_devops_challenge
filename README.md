# DevOps Challenge Setup

## Overview

This repository automates the provisioning and configuration of an AWS EC2 instance using Ansible and validates its setup using InSpec tests. The workflow is triggered on a push to the `feat/ansible-devops-vm` branch.

## Workflow Summary

### Steps Performed:

1. **Provision an EC2 Instance**

   - Uses AWS credentials to launch a new EC2 instance in `us-east-1`.
   - The instance is of type `t2.micro` and is launched with a specified AMI and security group.
   - Waits for the instance to reach the `running` state.
   - Retrieves the public IP address of the instance.

2. **Install Ansible on the EC2 Instance**

   - Connects to the instance via SSH.
   - Installs Ansible for configuration management.

3. **Run Ansible Playbook**

   - Executes `playbook.yml` on the EC2 instance to configure it.

4. **System Configuration by Ansible Playbook**
   The Ansible playbook performs the following tasks:

   - Installs **Nginx**, **Git**, and **Python3**.
   - Disables root login via SSH.
   - Creates a `devops` user.
   - Adds the `devops` user to the `sudoers` group.
   - Generates an SSH key for the `devops` user.
   - Restarts the SSH and Nginx services to apply changes.

5. **Verify Configuration with InSpec**

   - Installs InSpec on the GitHub Actions runner.
   - Runs `inspec_test.rb` against the EC2 instance to validate the following:
     - Nginx is installed.
     - The instance is correctly configured as per security and service requirements.
   - If any InSpec test fails, the workflow exits with an error.

## Prerequisites

To use this workflow, ensure the following secrets are configured in the repository settings:

- `AWS_ACCESS_KEY_ID`: AWS Access Key ID
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Access Key
- `AWS_REGION`: AWS Region
- `AWS_SSH_KEY_NAME`: Name of the SSH key used for EC2 access
- `AWS_SSH_PRIVATE_KEY`: Private SSH key for accessing the EC2 instance

## Running the Workflow

To trigger the workflow:

- Push changes to the `feat/ansible-devops-vm` branch.
- The workflow will automatically run, provisioning an EC2 instance, configuring it with Ansible, and validating it using InSpec.

## Output

- A running EC2 instance configured with Nginx, Git, Python3, and a `devops` user with SSH access.
- InSpec tests ensuring compliance with the required setup.
- The workflow will fail if any step (Ansible configuration or InSpec tests) encounters an error.

## Notes

- Modify `playbook.yml` to customize the installed services and configurations.
- Update `inspec_test.rb` to validate additional configurations as needed.
- Ensure that the specified AMI ID is valid for the selected AWS region.
- Future improvements:
  - Add InSpec tests to verify that **Python3** and **Git** are installed.
  - Install InSpec directly on the EC2 instance so that tests can be run via Ansible instead of SSH.

## Pre-commit Configuration

To enforce coding standards, a `.pre-commit-config.yaml` file can be used for linting and whitespace checks. Below is a simple configuration:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
```

Run manually before committing:

1.
   ```bash
   pre-commit run --all-files
   ```
