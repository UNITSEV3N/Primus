
# Go to the project root (one directory above scripts/)
cd "$(dirname "$0")/.." || exit 1

# Enable the environment
source .venv/bin/activate

# Run the bot
python -B -m bot.main

