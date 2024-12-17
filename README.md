![Screenshot 2024-12-17 155736](https://github.com/user-attachments/assets/4995d91e-75a8-4a9b-9c47-a328761c72ca)![Screenshot 2024-12-17 155618](https://github.com/user-attachments/assets/bdf63456-c1d4-4a95-b365-9ffbd4936d15)# Book Recommendation System Assistant

This project is a book recommendation system that leverages the Google Books API to recommend books based on user preferences such as genre, author, or keywords. It features a backend service built with FastAPI and a frontend interface developed using Streamlit for interactive user input. Additionally, it incorporates the OpenAI Assistant API to assist with user queries, providing an AI-powered chatbot experience for enhanced user interaction and personalized recommendations.

## Streamlit Front-End

- Click here to View ![Streamlit Front-End](https://book-recommendation-system.replit.app/)

https://github.com/user-attachments/assets/6a2a3ef7-e72c-4089-b519-093d3de0edb9

![book-recommendation-system](https://github.com/user-attachments/assets/3652466a-830c-4441-b056-6bee6fced15e)

## React Front-End

- Click here to View ![React Front-End](https://book-recommendation-system-react-app.replit.app/)

![Screenshot 2024-12-17 155618](https://github.com/user-attachments/assets/025e8a3b-cc87-46e3-9c39-aacb3ef66585)

![Screenshot 2024-12-17 155657](https://github.com/user-attachments/assets/0d8ba768-ab43-4698-8230-bf29e182ce55)

![Screenshot 2024-12-17 155736](https://github.com/user-attachments/assets/1528e684-807a-4837-bc3d-e559d7ed67dc)

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
   - On Windows:
      - myenv\Scripts\activate
   - On macOS/Linux:
      - source myenv/bin/activate

4. Install the required dependencies:
   - pip install -r requirements.txt

5. Running the Backend (Start the FastAPI server)
   - myenv\Scripts\activate
   - python main.py
     
6. The backend will be running at http://localhost:8000.

## Running the Frontend (Streamlit)

1. Open New Terminal & Start the Streamlit frontend:
   - myenv\Scripts\activate 
   - streamlit run frontend.py
     
2. The frontend will be running at http://localhost:8501.

3. The frontend will open in your browser, where you can provide inputs like genre and receive book recommendations.

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
- OpenAI Assistant API: Used for assistance with user queries
