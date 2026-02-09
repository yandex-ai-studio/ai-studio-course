#!/bin/bash

# ============================================
# Yandex Cloud Service Account Setup Script
# Creates SA with ai.editor role and .env file
# ============================================

set -e

SA_NAME="ai-studio-sa"
ENV_FILE=".env"

echo "=== Yandex Cloud Service Account Setup ==="
echo

# Check if yc CLI is installed
if ! command -v yc &> /dev/null; then
    echo "ERROR: Yandex Cloud CLI (yc) is not installed or not in PATH"
    echo "Install it from: https://cloud.yandex.ru/docs/cli/quickstart"
    exit 1
fi

# Get current folder_id
echo "Getting folder_id..."
FOLDER_ID=$(yc config get folder-id 2>/dev/null || echo "")

if [ -z "$FOLDER_ID" ]; then
    echo "ERROR: folder-id is not configured in yc CLI"
    echo "Run: yc init"
    exit 1
fi
echo "Folder ID: $FOLDER_ID"

# Check if service account already exists
echo
echo "Checking if service account \"$SA_NAME\" exists..."
SA_ID=$(yc iam service-account get --name "$SA_NAME" --format json 2>/dev/null | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4 || echo "")

if [ -z "$SA_ID" ]; then
    echo "Creating service account \"$SA_NAME\"..."
    SA_ID=$(yc iam service-account create --name "$SA_NAME" --format json | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)
else
    echo "Service account already exists."
fi

if [ -z "$SA_ID" ]; then
    echo "ERROR: Failed to get service account ID"
    exit 1
fi
echo "Service Account ID: $SA_ID"

# Assign ai.editor role
echo
echo "Assigning ai.editor role to the service account..."
if yc resource-manager folder add-access-binding \
    --id "$FOLDER_ID" \
    --role ai.editor \
    --subject "serviceAccount:$SA_ID" 2>/dev/null; then
    echo "Role ai.editor assigned successfully"
else
    echo "Warning: Role might already be assigned or insufficient permissions"
fi

# Create API key
echo
echo "Creating API key..."
API_KEY=$(yc iam api-key create --service-account-name "$SA_NAME" 2>/dev/null | grep "secret:" | awk '{print $2}')

if [ -z "$API_KEY" ]; then
    echo "ERROR: Failed to create API key"
    exit 1
fi
echo "API key created successfully"

# Create .env file
echo
echo "Creating $ENV_FILE file..."
cat > "$ENV_FILE" << EOF
folder_id=$FOLDER_ID
api_key=$API_KEY
EOF

echo
echo "=== Setup Complete ==="
echo
echo "Created $ENV_FILE with:"
echo "  - folder_id=$FOLDER_ID"
echo "  - api_key=***hidden***"
echo
echo "Service account \"$SA_NAME\" is ready to use."
