# image-tagger
Image-tagger is an efficent and easy-to-use web-based application for visually tagging large numbers of images with data. Intended for users who have a need to manually review images, it automates displaying each user to the image and allows them to enter data for that image with minumal user input.

## Installation

Image-tagger requires Python 3, Flask and Python-Magic. 

### Linux

Install dependencies.

* Ubuntu/Debian: `sudo apt install git python3 python3-flask python3-magic`

Clone the image-tagger repository.

```
git clone https://github.com/TaxaList/image-tagger.git
```

### Windows

Install the latest version of [Python 3](https://www.python.org/) and [Git](https://git-scm.com/).

Clone the image-tagger repository.

```
git clone https://github.com/TaxaList/image-tagger.git
```

## Useage

Place images to be tagged in `image-tagger/images`.

From the `image-tagger` directory, run:

```
python app.py
```

The application will be available at [http://localhost:8080](http://localhost:8080).