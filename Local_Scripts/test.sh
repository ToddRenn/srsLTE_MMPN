#!/bin/bash
parent=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P)
echo "${parent}"

cd "${parent}"

echo "Hello" > txt
