#!/bin/bash

cloudflared access tcp --hostname db-tunnel-dev.soleiljoy.com --url localhost:3307 &

clear

