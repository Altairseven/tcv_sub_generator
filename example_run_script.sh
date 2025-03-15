#!/bin/bash
# tcv_subs wrapper script

# Resolve relative input and output paths to absolute paths
INPUT_FOLDER=$(realpath "./Inbox")
OUTPUT_FOLDER=$(realpath "./Outbox")

# Call the Python script with the resolved paths
python "[ADD FULL PATH]/tcv_subs.py" "$INPUT_FOLDER" "$OUTPUT_FOLDER"