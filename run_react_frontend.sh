#!/bin/bash
# Run React frontend

cd "$(dirname "$0")" || exit 1

echo "Starting BB84 QKD React Frontend..."
echo "Frontend available at: http://localhost:3000"
echo ""
echo "Make sure the backend is running:"
echo "  ./run_backend.sh"
echo ""

cd bb84-react-frontend
npm run dev "$@"
