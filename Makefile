.PHONY: setup db-up db-down run clean

# Install dependencies using uv
setup:
	uv sync

# Start the database in the background
db-up:
	docker compose up -d

# Stop the database
db-down:
	docker compose down

# Start the database and run the application script
run: db-up
	uv run python main.py

# Clean up
clean: db-down
	rm -rf .venv
