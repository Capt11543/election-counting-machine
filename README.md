# Election Counting Machine

Welcome to the Election Counting Machine. This script has been designed for use by the Ministry of Internal Affairs of the [Kingdom of Alexandria](https://mcstatecraft.com). Citizens are also able to audit the elections using this script.

## Usage Guide

### For Alexandrian Elections

1. [Install Python](https://www.python.org/downloads/). If you are using Windows, make sure to add Python to your PATH directory when it gives you the option to.
2. Download or clone this repository. To download, click the green "<> Code" button and choose "Download ZIP". Extract the files, and make a note of where you extracted it to. If you are choosing to clone the repository instead of downloading the code, I will assume you already know how to do that.
3. Log on to the StateCraft Minecraft server and open the Elections Manager by running `/elections`. Locate the election you are adjudicating and make a note of its ID number.
4. Export the ballot data from the DemocracyElections plugin by running the command `/elections export ballots online <id_number>`.
5. Open the resulting GitHub link, and click "Download ZIP" in the top-right corner.
6. Extract the downloaded ZIP file, and locate the file named `ballots-<id_number>.json`. Drop the file into the same folder as `election_counting_machine.py`.
7. In #commands of the StateCraft discord, run the Utilities bot's `/random` command. For best results, set `min_value` to `0` and `max_value` to a very high number (e.g. `999999`). Save a link to the resulting message for the transparency report.
8. Open a terminal (e.g. Command Prompt or PowerShell) in the same folder as `election_counting_machine.py`,
   On Windows 11, right-click on any empty space in the File Explorer window and select "Open in Terminal".
9. Run the script by typing `python election_counting_machine.py` into the terminal and pressing ENTER.
10. Follow the instructions to ensure the script runs properly.
    Enter the random number you generated in step 4 as the seed.
    The path to the ballots should simply be the name of the .json file containing the ballot data (including the ".json" extension) if you placed said .json file properly in step 6.
    The results will be output to a file named `<currenttime>_vote_count.txt` for easy publishing.
11. To ensure full legal compliance, compress the entire folder containing `election_counting_machine.py` and attach it to the transparency report.
