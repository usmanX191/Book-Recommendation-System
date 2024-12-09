import asyncio
import os
import random
import re

import openai
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
from pydantic import BaseModel
from termcolor import colored

# Load environment variables from .env file
load_dotenv()
client = OpenAI()
app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


def fetch_books(query=None, author=None, title=None):
    """
    Fetches book data from Google Books API.

    :param query: General search query string
    :param author: Author name to refine the search
    :param title: Title of the book to refine the search
    :param max_results: Maximum number of results to fetch
    :return: List of books fetched from the API
    """
    url = "https://www.googleapis.com/books/v1/volumes"

    random_start_index = random.randint(0, 40)  # Adjust based on API constraints

    # Build the search query
    search_query = ""
    if query:
        search_query += query
    if author:
        search_query += f" inauthor:{author}"
    if title:
        search_query += f" intitle:{title}"

    params = {
        "q": search_query.strip(),
        "maxResults": 10,
        "minResults": 3,
        "startIndex": random_start_index,
        "key": API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Debug log for fetched books
        if "items" in data:
            print(colored(f"Fetched {len(data['items'])} books from the API.", "green"))

        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        print(colored(f"Error fetching data: {e}", "red"))
        return []


def add_space_before_punctuation(text):
    """Adds a space before punctuation marks if not already present."""
    return re.sub(r"(?<!\s)([?.!,;])", r" \1", text)


def display_books(books):
    """
    Display details of the first 20 books.
    """
    print(colored(f"Displaying Books {books}:\n", "green"))
    print(colored(f"Displaying first {len(books)} results:\n", "green"))
    print(colored("Books:", "green"))
    for i, book in enumerate(books, start=1):
        title = book.get("volumeInfo", {}).get("title", "No Title")
        authors = book.get("volumeInfo", {}).get("authors", ["Unknown Author"])
        published_date = book.get("volumeInfo", {}).get("publishedDate", "No Date")
        description = book.get("volumeInfo", {}).get("description", "No Description")

        print(colored(f"{i}. Title: {title}", "green"))
        print(colored(f"   Authors: {', '.join(authors)}", "green"))
        print(colored(f"   Published Date: {published_date}", "green"))
        print(colored(f"   Description: {description}\n", "green"))


async def get_keyword_from_chat(user_query, threadId):
    try:
        add_message = client.beta.threads.messages.create(
            thread_id=threadId,
            role="user",
            content=user_query,
        )
        print(colored(f"User Query added to thread: {add_message}", "green"))

        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistant_id,
        )
        print(colored(f"\nRun created: {run}", "green"))

        while True:
            run_object = openai.beta.threads.runs.retrieve(
                thread_id=threadId, run_id=run.id
            )
            print(colored(f"Run Object: {run_object}", "green"))
            print(colored(f"Run status: {run_object.status}", "green"))

            if run_object.status == "completed":

                messages_list = openai.beta.threads.messages.list(thread_id=threadId)
                messages = list(messages_list)

                # Extract messages for user and assistant
                def extract_text_content(message):
                    """Extract text content from a message."""
                    if message and message.content:
                        for block in message.content:
                            if block.type == "text":
                                return block.text.value
                    return None

                user_text = extract_text_content(
                    next((msg for msg in messages if msg.role == "user"), None)
                )
                print(colored(f"User Text: {user_text}", "green"))
                assistant_text = extract_text_content(
                    next((msg for msg in messages if msg.role == "assistant"), None)
                )
                print(colored(f"Assistant Text: {assistant_text}", "green"))
                return {
                    "query": user_text,
                    "response": assistant_text,
                    "status": run_object.status,
                    "run_id": run.id,
                }

            elif run_object.status == "failed":
                print(colored(f"Run failed: {run_object}", "red"))
                return {
                    "query": user_query,
                    "response": "def",
                    "status": run_object.status,
                    "run_id": run.id,
                }

            elif run_object.status == "requires_action":
                print(colored("Run requires action.", "yellow"))
                tool_calls = run_object.required_action.submit_tool_outputs.tool_calls

                for tool_call in tool_calls:
                    if (
                        tool_call.type == "function"
                        and tool_call.function.name == "fetch_books"
                    ):
                        user_info = eval(tool_call.function.arguments)
                        print(colored(f"User Info: {user_info}", "green"))

                        criteria = user_info.get(
                            "criteria", {}
                        )  # Extract the 'criteria' dictionary
                        genre = criteria.get("genre", "")  # Extract the 'genre' value
                        author = criteria.get(
                            "author", ""
                        )  # Extract the 'author' value
                        title = criteria.get("title", "")  # Extract the 'title' value
                        books = fetch_books(query=genre, author=author, title=title)
                        print(colored(f"Fetched Books: {books}", "green"))
                        books_data = []
                        # Display the fetched books
                        for i, book in enumerate(books, start=1):
                            title = book.get("volumeInfo", {}).get("title", "No Title")
                            authors = book.get("volumeInfo", {}).get(
                                "authors", ["Unknown Author"]
                            )
                            published_date = book.get("volumeInfo", {}).get(
                                "publishedDate", "No Date"
                            )
                            description = book.get("volumeInfo", {}).get(
                                "description", "No Description"
                            )
                            previewLink = book.get("volumeInfo", {}).get(
                                "previewLink", "No Link"
                            )
                            # Store book data in a dictionary
                            book_info = {
                                "id": i,
                                "title": title,
                                "authors": authors,
                                "published_date": published_date,
                                "description": description,
                                "previewLink": previewLink,
                                "genre": genre,
                            }

                            # Append to the list of books data
                            books_data.append(book_info)
                        print(colored(f"Books Data: {books_data}", "green"))

                        response = openai.beta.threads.runs.submit_tool_outputs(
                            thread_id=threadId,  # Corrected argument name
                            run_id=run.id,
                            tool_outputs=[
                                {
                                    "tool_call_id": tool_call.id,
                                    "output": (
                                        f"This is the Books Data: {books_data},\n"
                                        "Now kindly show the books to the user like in this format:\n"
                                        '    "1- title": title,\n'
                                        '    "2- authors": authors,\n'
                                        '    "3- published_date": published_date,\n'
                                        '    "4- description": description,\n'
                                        '    "5- previewLink": previewLink,\n'
                                        "But Kindly Please Make sure that user can see all of these details or fields of the books."
                                    ),
                                }
                            ],
                        )

                        print("toolCall.id:", tool_call.id)
                        print("Response:", response)

                        return {
                            "query": user_query,
                            "response": "def",
                            "status": run_object.status,
                            "run_id": run.id,
                        }

            await asyncio.sleep(5)
    except Exception as e:
        print(colored(f"Error: {e}", "red"))
        return {}


# Models for Request and Response
class ChatRequest(BaseModel):
    query: str
    thread_id: str


class ThreadResponse(BaseModel):
    thread_id: str


@app.get("/")
async def read_root():
    """
    Creates a new chat thread.
    """
    try:
        return {"message": "Welcome to the Book Recommendation System & Chatbot!"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/thread", response_model=ThreadResponse)
async def create_thread():
    """
    Creates a new chat thread.
    """
    try:
        print(colored("Page is Reloaded !!!", "green"))
        print(colored("Creating a new thread...", "green"))
        new_thread = client.beta.threads.create()
        thread_id = new_thread.id
        print(colored(f"New thread created: {thread_id}", "green"))
        return {"thread_id": new_thread.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Handles chat requests and fetches responses.
    """

    print(colored("New Chat Message Requested !!!", "green"))
    user_query = add_space_before_punctuation(request.query)
    print(colored(f"User Query: {user_query}", "green"))
    thread_id = request.thread_id
    print(colored(f"Thread ID: {thread_id}", "green"))
    if not thread_id:
        raise HTTPException(status_code=400, detail="Thread ID is required.")

    result = await get_keyword_from_chat(user_query, thread_id)
    query = result.get("query", "No query")
    response = result.get("response", "No response available")
    result_status = result.get("status", "No status available")
    run_id = result.get("run_id", "No run ID available")
    if result_status == "completed":
        return JSONResponse(content={"response": f"{response} "})

    elif result_status == "requires_action":
        while True:
            run_object = openai.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
            print(colored(f"Run Object: {run_object}", "green"))
            print(colored(f"Run status: {run_object.status}", "green"))

            if run_object.status == "completed":

                messages_list = openai.beta.threads.messages.list(thread_id=thread_id)
                messages = list(messages_list)

                # Extract messages for user and assistant
                def extract_text_content(message):
                    """Extract text content from a message."""
                    if message and message.content:
                        for block in message.content:
                            if block.type == "text":
                                return block.text.value
                    return None

                user_text = extract_text_content(
                    next((msg for msg in messages if msg.role == "user"), None)
                )
                print(colored(f"User Text: {user_text}", "green"))
                assistant_text = extract_text_content(
                    next((msg for msg in messages if msg.role == "assistant"), None)
                )
                print(colored(f"Assistant Text: {assistant_text}", "green"))
                return JSONResponse(content={"response": f"{assistant_text} "})
            if run_object.status == "failed":
                assistant_text = "Sorry, I am unable to process your request at the moment. Please try again later or reload the page and start a new chat again."
                return JSONResponse(content={"response": f"{assistant_text} "})
            await asyncio.sleep(5)
    elif result_status == "failed":
        assistant_text = "Sorry, I am unable to process your request at the moment. Please try again later or reload the page and start a new chat again."
        return JSONResponse(content={"response": f"{assistant_text} "})


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
