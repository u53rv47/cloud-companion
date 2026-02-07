name: Bug Report
description: Report a bug to help us improve
title: "[BUG] "
labels: ["bug", "needs-triage"]

body:

- type: markdown
  attributes:
  value: |
  Thanks for taking the time to report this bug!

- type: textarea
  attributes:
  label: Description
  description: Clear description of what the bug is
  placeholder: Describe the issue...
  validations:
  required: true

- type: textarea
  attributes:
  label: Steps to Reproduce
  description: Steps to reproduce the behavior
  placeholder: | 1. 2. 3.
  validations:
  required: true

- type: textarea
  attributes:
  label: Expected Behavior
  description: What you expected to happen
  validations:
  required: true

- type: textarea
  attributes:
  label: Actual Behavior
  description: What actually happened

- type: textarea
  attributes:
  label: Environment
  description: Environment details
  placeholder: | - OS: [e.g., Linux, macOS, Windows] - Python version: [e.g., 3.10.5] - Cloud Companion version: [e.g., 0.1.0]
  validations:
  required: true

- type: textarea
  attributes:
  label: Logs/Error Messages
  description: Any relevant error messages or logs

- type: checkboxes
  attributes:
  label: Checklist
  options: - label: I've searched for existing issues
  required: true - label: I'm using the latest version
  required: true
