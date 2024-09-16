# Space Fighter Game

## Overview

**Space Fighter** is an engaging and action-packed space shooter game developed using Python's Kivy and Pygame libraries. Players take control of a fighter plane navigating through space, battling enemies, and collecting power-ups to achieve the highest possible score. The game features responsive multi-directional movement, dynamic enemy spawning, various power-ups, and stunning visual effects to enhance the gaming experience.

## Features

- **Responsive Movement**: Smooth and fast movement in all directions with support for diagonal controls.
- **Shooting Mechanics**: Fire bullets with adjustable angles based on power-up levels.
- **Power-Ups**: Collect power-ups such as Shield, Rapid Fire, Bomb, and Speed Boost to gain temporary advantages.
- **Dynamic Enemies**: Enemies spawn at varying intervals and increase in difficulty over time.
- **Particle Effects**: Enjoy visually appealing explosions and particle effects when enemies are destroyed.
- **Sound Effects & Music**: Immersive audio experience with sound effects for shooting, explosions, power-ups, and background music.
- **Game Over Screen**: Display final score with options to restart or quit the game.
- **Android Deployment**: Package the game for Android devices using Buildozer and Docker.

## Screenshots

*Include screenshots of the game here to showcase gameplay, UI, and features.*

## Getting Started

### Prerequisites

- **Python 3.6+**
- **Kivy**
- **Pygame**
- **Buildozer** (for Android deployment)
- **Docker** (optional, for using the Buildozer Docker container)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/space-fighter.git
   cd space-fighter
   ```

2. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install kivy pygame
   ```

   *If a `requirements.txt` is provided, use:*

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Assets Are in Place**

   Make sure all assets (images, sounds, etc.) are located in the `assets/` directory as referenced in the code.

## Running the Game

To run the game locally:

bash
python main.py

```

## Controls

- **Arrow Keys**: Move the fighter plane up, down, left, and right.
- **Spacebar**: Shoot bullets.
- **Escape**: Quit the game.

## Power-Up Types

1. **Shield**: Grants temporary immunity against enemy collisions.
2. **Rapid Fire**: Increases the rate of fire.
3. **Bomb**: Destroys all enemies on the screen.
4. **Speed Boost**: Temporarily increases the fighter's movement speed.

## Building for Android

### Using Buildozer with Docker

A `docker-compose.yml` is provided to simplify the Buildozer setup using Docker.

1. **Ensure Docker is Installed**

   Download and install Docker from [Docker's official website](https://www.docker.com/get-started).

2. **Configure Buildozer Environment**

   Adjust the `docker-compose.yml` file if necessary, ensuring that the `ANDROIDSDK` and `ANDROIDNDK` paths are correctly set.

3. **Build the APK**

   ```bash
   docker-compose up --build
   ```

   This command builds the APK and places it within the project directory upon successful completion.

### Direct Buildozer Installation

Alternatively, you can install Buildozer directly on your system:

```bash
pip install buildozer
sudo apt update
sudo apt install -y git python3-pip build-essential \
    python3-dev python3-venv git-core \
    openjdk-8-jdk unzip zlib1g-dev
```

Initialize Buildozer and build the APK:

```bash
buildozer init
buildozer -v android debug
```

*For detailed instructions, refer to the [Buildozer documentation](https://buildozer.readthedocs.io/en/latest/).*

## Project Structure

```
Space Fighter/
├── assets/
│   ├── sounds/
│   ├── spaceArt/
│   │   ├── png/
│   │   └── spaceArt.ai
│   └── ...
├── src/
│   ├── game.py
│   ├── game_objects.py
│   ├── constants.py
│   └── particle.py
├── main.py
├── SpaceFighter.kv
├── buildozer.spec
├── docker-compose.yml
├── Readme.md
└── .gitignore
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Submit a pull request detailing your changes.

## TODO
- Make it available on web
- Fix issue with the speed of the fighter plane
- Introduce more levels
- Power-ups for enemies
- Add achievements
- Implement leaderboard
- Improve graphics
- Optimize performance
- Add more sound effects


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- **Kivy**: For providing a robust framework for building cross-platform applications.
- **Pygame**: For enabling game development in Python.
- **Buildozer**: For simplifying Android deployment.
- **OpenAI**: For assistance in code optimization and project guidance.

## Contact

For any questions or suggestions, please reach out to [waqaskhan137@gmail.com](mailto:waqaskhan137@gmail.com).
