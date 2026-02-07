name: Feature Request
description: Suggest an idea for this project
title: "[FEATURE] "
labels: ["enhancement", "needs-triage"]

body:

- type: markdown
  attributes:
  value: |
  Thanks for your interest in improving Cloud Companion!

- type: textarea
  attributes:
  label: Description
  description: Clear description of the feature
  placeholder: Describe what you'd like to see...
  validations:
  required: true

- type: textarea
  attributes:
  label: Use Case
  description: Why would this feature be useful?
  placeholder: Explain the use case...
  validations:
  required: true

- type: textarea
  attributes:
  label: Proposed Solution
  description: How do you envision this feature working?
  placeholder: Describe the solution...

- type: textarea
  attributes:
  label: Alternatives
  description: Any alternative approaches?

- type: checkboxes
  attributes:
  label: Checklist
  options: - label: I've searched for similar feature requests
  required: true
