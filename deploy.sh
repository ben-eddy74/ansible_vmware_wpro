#!/usr/bin/bash
ansible-galaxy collection build --force
ansible-galaxy collection install . --force
