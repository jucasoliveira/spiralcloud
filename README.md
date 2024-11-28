# Spiral Animation Metrics Visualization

This project visualizes the performance of various programming languages in rendering a spiral animation by using recorded metrics. The animation showcases balls representing different programming languages moving back and forth horizontally, where the speed is determined by the average frame time.

## Project Overview

The script reads performance metrics from `.txt` files, such as `Frame Time` and `Points Drawn`, for each programming language implementation. It calculates the average values and visualizes them in an animation using Matplotlib. Each language is represented by a ball that moves across a horizontal line, where the speed of each ball is proportional to the average frame time. The balls are also color-coded to differentiate between the languages.

### Features

- **Metrics Extraction**: Reads `Frame Time` and `Points Drawn` from `.txt` files for each programming language.
- **Data Visualization**: Displays an animated graph where balls represent different languages and move back and forth based on their rendering performance.
- **Customizable Animation**: Balls are color-coded, and their speed can be adjusted based on the metrics.

## Project Structure

```
.
├── LICENSE
├── README.md
├── c
│   ├── metrics_c.txt
│   ├── spiral
│   └── spiral_sdl2.c
├── go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   └── metrics_go.txt
├── language_animation.mp4
├── metrics.py
├── node
│   ├── bun.lockb
│   ├── index.html
│   ├── index.js
│   ├── metrics_node.txt
│   ├── node_modules
│   ├── package.json
│   └── spiral.js
├── python
│   ├── metrics_python.txt
│   └── spiral.py
└── rust
    ├── Cargo.lock
    ├── Cargo.toml
    ├── metrics_rust.txt
    ├── src
    └── target
```

### Metrics Format

Each metrics file should be named with the following format: `metrics_<language>.txt` and contain lines like:

```
Frame Time: <time> ms, Points Drawn: <number>
```

For example:

```
Frame Time: 13 ms, Points Drawn: 9591
Frame Time: 12 ms, Points Drawn: 9585
...
```

## Metrics result

![Metrics result](./language_animation.mp4)

## Usage

1. **Install Dependencies**

   - Ensure you have Python 3.6+ installed.
   - Install the required Python libraries by running:
     ```sh
     pip install numpy matplotlib pillow
     ```

2. **Run the Metrics Script**
   - Place your metrics `.txt` files in the same directory as `metrics.py`.
   - Run the script to create the animation:
     ```sh
     python metrics.py
     ```
   - The animation will be saved as `languages_animation.mp4` in the current directory.

## Visualization Details

- **Languages Sorted by Speed**: The languages are sorted from fastest to slowest based on their average frame time.
- **Ball Animation**: Each language is represented by a ball, whose movement speed is determined by the average frame time.
- **Ball Size and Color**: Ball size is doubled for better visibility, and each language is color-coded to make the animation visually distinguishable.

## Dependencies

- **NumPy**: Used for numerical operations.
- **Matplotlib**: Used for creating the animation.
- **Pillow**: Used for saving the animation as a video.

## Troubleshooting

- **`MovieWriter ffmpeg unavailable`**: If you encounter this error, make sure you have `ffmpeg` installed, or use the `pillow` writer as done in this script.
- **Matplotlib Warning**: The `get_cmap` function has been deprecated in newer versions of Matplotlib. The script has been updated to use the recommended approach.

## License

This project is open source and available under the MIT License.
