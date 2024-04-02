# Image Color Palette Generator

This is a Flask web application that generates a color palette from an uploaded image. It provides the all occurring colors in the image.

## Features

- Upload an image to generate its color palette.
- Choose between hexadecimal or RGB color codes.

## Requirements

- Python 3.x
- Flask
- Pillow (PIL Fork)
- NumPy
- PostgreSQL

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
3. Set up a PostgreSQL database with the following configuration:
- Database name: [Your_database_name]
- User: [Your_database_user]
- Password: [Your_database_password]
- Host: [Your_database_host]
- Port: [Your_database_port]
4. Run the Flask application:
5. Access the application in your web browser at http://localhost:5000.

## Usage

1. Register an account or login if you already have one.
2. Upload an image on the homepage.
3. Select the color code format (Hexadecimal or RGB).
4. Click on "Generate Palette" to view the color palette.

## Database Schema

- Table: users
- Columns: id (Primary Key), username, password

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
