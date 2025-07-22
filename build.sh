#!/bin/bash

set -o errexit

acme -o dead_test.bin dead_test.a
python checksum.py
cartconv -t ulti -i dead_test.bin -o dead_test.crt
echo ""
echo "Done. Start with: x64sc -cartcrt dead_test.crt"
