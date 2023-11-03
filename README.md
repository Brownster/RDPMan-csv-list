# CSV Processing Web Application

This web application is built with Flask and allows users to upload a CSV file, process it according to specific business logic, and download the resulting CSV. It's designed to filter and export data related to Windows servers by looking for a match key in the CSV.

## Features

- Upload a CSV file to process.
- Input a match key to filter the data.
- Download the processed CSV with selected data fields.

## Installation

To get started with this application, you'll need to set up a Python environment and install the necessary dependencies.

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:

```bash
git clone https://your-repository-url.git
cd your-repository-directory

    Create a virtual environment:

bash

python -m venv venv

    Activate the virtual environment:

    On Windows:

bash

venv\Scripts\activate

    On MacOS/Linux:

bash

source venv/bin/activate

    Install the dependencies:

bash

pip install -r requirements.txt

Usage

To run the application:

bash

flask run

Access the web interface by navigating to http://127.0.0.1:5000/ in your web browser.
