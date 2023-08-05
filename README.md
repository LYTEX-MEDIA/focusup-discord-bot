## FocusUp Discord Integration

A Discord client that gets user data from FocusUp via RestAPIs.
There are also features like a DM-based ticket system using Sqlite3 as database.

## Setup
1. Install Python 3.6 or higher
2. Install the required packages with `pip install -r requirements.txt`
3. Create a file called `.env` in the root directory of the project
4. Fill the `.env` file with the following:
```DISCORD_SECRET_TOKEN=<your discord bot token>```
5. Run the bot with `python main.py`

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.