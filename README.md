# Helmet Detection Application

This application is designed to detect whether a person is wearing a helmet in real-time.

## Model

The application is trained using the YOLOv5 model.

## How to Run

To run the application in real-time, follow these steps:

1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Load the `best.pt` model file into the application.
3. Run the application script for real-time detection: `python detect.py --weights best.pt --source 0`

## Dependencies

Ensure you have the following dependencies installed:

- Python 3.10
- PyTorch
- OpenCV

## Usage

Once the application is running, it will process the input source (e.g., webcam) in real-time to detect and indicate if a person is wearing a helmet.

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests.
