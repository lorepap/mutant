#!/bin/bash

# Check if g++ is installed
if ! [ -x "$(command -v g++)" ]; then
    echo "Error: g++ is not installed." >&2
    exit 1
fi

# Compile server
g++ -o server server.cc
if [ $? -ne 0 ]; then
    echo "Compilation of server failed"
    exit 1
fi
echo "Server compiled successfully"

# Compile client
g++ -o client client.cc
if [ $? -ne 0 ]; then
    echo "Compilation of client failed"
    exit 1
fi
echo "Client compiled successfully"

echo "Build completed"
