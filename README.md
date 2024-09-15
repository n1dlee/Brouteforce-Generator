# Enhanced Dictionary Creator

## Description

The Enhanced Dictionary Creator is a Python application with a graphical user interface that allows users to generate custom dictionaries. It supports both numerical and alphabetical sequence generation, providing a user-friendly interface for creating large sets of sequential data.

## Features

- Generate numerical or alphabetical sequences
- Custom range selection for sequence generation
- Progress bar for real-time generation feedback
- System information display (CPU and GPU)
- Output directory selection
- Efficient caching for repeated alphabetical sequence generation

## Requirements

- Python 3.7+
- customtkinter
- psutil
- GPUtil (optional, for GPU information)

## Installation

1. Clone this repository or download the source code.

2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

1. Run the application:

```
python app.py
```

2. Select the generation mode (Number or Alphabet).

3. Enter the start and end values for your sequence.

4. Choose an output directory.

5. Click "Generate Dictionary" to create your custom dictionary file.

## System Requirements

- The application should run on any system with Python 3.7 or higher.
- GPU information display requires a NVIDIA GPU and the GPUtil library.

## Known Issues

- GPU detection may not work on all systems or with non-NVIDIA GPUs.
- Very large sequences may consume significant memory and processing time.

## Contributing

Contributions to the Enhanced Dictionary Creator are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please open an issue in the GitHub repository.
