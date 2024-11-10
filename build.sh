#!/bin/bash
set -e

# Build testcase-controller image
if ! docker buildx build --platform "linux/amd64" -t balicamihai/testcase-controller:amd64-7 -f docker/Dockerfile.testcase-controller . --push; then
  echo "Failed to build testcase-controller image"
  exit 1
fi

# # Build testcase-controller image
# if ! docker buildx build --platform "linux/arm64" -t balicamihai/testcase-controller:arm64-5 -f docker/Dockerfile_arm64.testcase-controller . --push; then
#   echo "Failed to build testcase-controller image"
#   exit 1
# fi