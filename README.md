# Book Recommendation System Assistant

This project is a book recommendation system that uses the Google Books API to recommend books based on user preferences such as genre, author, or keywords. It provides a backend service built with FastAPI and a frontend interface using Streamlit for interactive user input.

## Project Workflow

### Input
- User provides preferences such as:
- Genre (e.g., "fantasy," "science fiction," "romance")
- Optional author or keyword filter

### Processing
- Query the Google Books API using the provided genre and optional filters.
- Extract and format relevant book details like title, author, description, and average rating.

### Output
- Return a list of book recommendations, including:
- Title, author, genre
- A brief description
- Average rating (if available)

## Files in the Project

- **main.py**: Backend file using FastAPI to handle API requests for fetching book recommendations.
- **frontend.py**: Frontend file using Streamlit to provide an interactive UI for the user to enter preferences.
- **requirements.txt**: List of dependencies required for the project.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **.env**: Environment variables for sensitive information like API keys.
- **__pycache__**: Compiled Python files.
- **myenv**: Virtual environment folder for the project.

## How to Run the Project

### Prerequisites

Make sure you have the following installed:
- Python 3.x
- Streamlit
- FastAPI
- Google Books API access (for fetching book data)

### Setup

1. Clone this repository to your local machine.
2. Navigate to the project folder and create a virtual environment:
   - python -m venv myenv

3. Activate the virtual environment:
   - On Windows: myenv\Scripts\activate
   - On macOS/Linux: source myenv/bin/activate

4. Install the required dependencies:
   - pip install -r requirements.txt

5. Running the Backend (FastAPI)
   - Start the FastAPI server:
   - uvicorn main:app --reload

6. The backend will be running at http://127.0.0.1:5000.

## Running the Frontend (Streamlit)

1. Start the Streamlit frontend:
   - streamlit run frontend.py

2. The frontend will open in your browser, where you can provide inputs like genre and receive book recommendations.

## Example Output

For user input like "Recommend books in the fantasy genre," the output will look something like this:

1. The Hobbit by J.R.R. Tolkien

   - Description: Bilbo Baggins embarks on an epic journey...
   - Rating: 4.7
   - More Info: The Hobbit

2. Harry Potter and the Sorcerer's Stone by J.K. Rowling

   - Description: A young wizard begins his magical education...
   - Rating: 4.8
   - More Info: Harry Potter

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google Books API: Used for fetching book data.
- FastAPI: Used for backend development.
- Streamlit: Used for frontend development.
