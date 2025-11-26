#!/bin/bash
# GJH Blog Agent - Stop Script

echo "Stopping GJH Blog Agent..."
docker compose down

echo ""
echo "All services stopped."
echo ""
echo "To remove all data (WARNING: This deletes everything!):"
echo "  docker compose down -v"
echo ""
