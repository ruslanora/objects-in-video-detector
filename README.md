# objects-in-video-detector

A proof-of-concept microservice that detects objects in video files using a pre-trained Faster R-CNN model with a ResNet-50 backbone.

## Requirements

- Python
- Docker (Optional)

## Getting Started

### Environment Variables

Create a `.env` file and place it in the root directory.

See [.env.example](.env.example) for the list of variables.

### Using Docker

`cd` to the project directory and run a docker container:

```sh
make serve
```

### Using venv


`cd` to the project directory and create a virtual environment:

```sh
make venv
```

Enter the environment by running:

```sh
source venv/bin/activate
```

Install dependencies:

```sh
make install
```

Run the server:

```sh
make dev
```

## How to Use

### Input

The service provides one API endpoint (`0.0.0.0:8000/vision`) that accepts `POST` requests with `multipart/form-data` content type.

Here's an example of a `curl` request:

```sh
curl -X POST "http://localhost:8000/vision" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/input/file.mp4;type=video/mp4"
     -o /path/to/output/file.csv
```

Replace `/path/to/input/file.mp4` and `/path/to/output/file.csv` with your file paths.

### Output

The output is a CSV file that includes the following data/columns:

- `timestamp`: a timestamp of a frame in seconds
- `label`: a COCO category
- `score`: confidence score between 0 and 1
- `x_min`, `y_min`, `x_max`, and `y_max`: bounding box coordinates

See [an example output file](results.example.csv]) for more.

## Contributing

Install all development dependencies by running:

```sh
make install-dev
```

Set up git hooks by running:

```sh
make hooks
```

## License

[MIT License](LICENSE)

