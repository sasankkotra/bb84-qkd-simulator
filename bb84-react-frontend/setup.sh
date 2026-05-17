#!/bin/bash
set -e

echo "Installing dependencies for BB84 React Frontend..."
cd "$(dirname "$0")" || exit 1

if [ ! -d "node_modules" ]; then
    npm install
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start development server, run:"
echo "  npm run dev"
echo ""
echo "The app will be available at http://localhost:3000"
echo "Make sure the FastAPI backend is running on http://localhost:8000"
