# Election Counting Machine
Welcome to the Election Counting Machine.  This script has been designed for use by the Ministry of Internal Affairs of the [Kingdom of Alexandria](https://mcstatecraft.com).  Citizens are also able to audit the elections using this script.
## Usage Guide
### For Alexandrian Elections
1. [Install Python](https://www.python.org/downloads/).  If you are using Windows, make sure to add Python to your PATH directory when it gives you the option to.
2. Download or clone this repository.  (Click the green "<> Code" button.)  Extract the files if needed, and make a note of where you cloned/extracted it to.
3. Export the ballot data from the DemocracyElections plugin as a JSON file.  Drop the file into the same folder as `election_counting_machine.py`.
4. In #commands of the StateCraft discord, run the Utilities bot's `/random` command.  For best results, set `min_value` to `0` and `max_value` to a very high number (e.g. `999999`).  Save a link to the resulting message for the transparency report.
5. Open a terminal (e.g. Command Prompt or PowerShell) in the same folder as `election_counting_machine.py` and run the script (`python election_counting_machine.py`).
6. Follow the instructions to ensure the script runs properly.  The results will be output to a file named `<currenttime>_vote_count.txt` for easy publishing.
7. To ensure full legal compliance, compress the entire folder containing `election_counting_machine.py` and attach it to the transparency report.
