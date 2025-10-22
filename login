#!/bin/bash

set -o xtrace
ssh-add
gh auth login -p ssh -h Github.com --skip-ssh-key -w
gcloud auth login