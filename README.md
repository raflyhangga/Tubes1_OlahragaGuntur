# Tubes1_OlahragaGuntur

This project is for logical implementation for [💎 diamonds game](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0) using greedy strategy in order to get the maximum amount of diamond in a certain point of time. 

This bot implements a ***Price Per Length*** strategy in order to get the nearest diamond with the greatest value. 🤑🤑🤑 

# Running the Bot 🏃🏻‍♂️
1. Make sure that you have the **Game Engine** installed and running properly.
2. The main logic for this repository is from ```botRafly.py``` with the logic called **RAFLY**.
3. Open a terminal in ```bot_starterpack``` folder.
4. To run one bot

    ```
    python main.py --logic RAFLY --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```
5. To run multiple bots simultaneously

    For Windows

    ```
    ./run-bots.bat
    ```

    For Linux / (possibly) macOS

    ```
    ./run-bots.sh
    ```

    <b>Before executing the script, make sure to change the permission of the shell script to enable executing the script (for linux/macOS)</b>

    ```
    chmod +x run-bots.sh
    ```

## Note 📝:

-   If you run multiple bots, make sure each emails and names are unique
-   The email could be anything as long as it follows a correct email syntax
-   The name, and password could be anything without any space

# Credentials ©️
This repository is adapted from https://github.com/Etimo/diamonds2

Some code in this repository is adjusted to fix some issues in the original repository and to adapt to the requirements of Algorithm Strategies course (IF2211), Informatics Undergraduate Program, ITB.

©️ All rights and credits reserved to [Etimo](https://github.com/Etimo)