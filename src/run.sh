#!/bin/bash

# Create connection to remote server
source runCloudflaredTunnel.bash

# Start the app
uv run -m webapp.app
