from celery import shared_task
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field
from typing import Iterable
import time
from .models import LLMTask

client = instructor.from_openai(OpenAI())

class Search(BaseModel):
    query: str = Field(description="Query to search for relevant content")
    search_type: str = Field(description="Type of search")

class Expand(BaseModel):
    data: str = Field(description="Data to go into more details")

class Answer(BaseModel):
    answer: str = Field(description="Answer to the question")

@shared_task()
def call_llm(search_input):
    """
    The main purpose of this task is to show an example of multistep long running task
    """
    start_time = time.time()  # Start time of the task

    # Save the initial search input in the LLMTask model
    current_llm_task = LLMTask.objects.create(search_input=search_input)

    # expanding search
    search_queries_start_time = time.time()
    search_queries = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_model=Iterable[Search],
        messages=[
            {
                "role": "user",
                "content": f"Consider the data below: '\n{search_input}' and segment it into multiple search queries",
            },
        ],
        max_tokens=1000,
    )
    print(f"Expanding search took {time.time() - search_queries_start_time} seconds")
    print(len(search_queries), "search queries")

    results = []

    # getting answers for each search query
    for query in search_queries:
        answer_start_time = time.time()
        result = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_model=Expand,
        messages=[
                {
                    "role": "user",
                    "content": f"Answer this question: '\n{query}'",
                },
            ],
            max_tokens=1000,
        )
        print(f"Getting answer for query took {time.time() - answer_start_time} seconds")

        results.append(result)
    
    # creating a prompt with everything
    prompt_creation_start_time = time.time()
    prompt = f"Original Search Input: {search_input}\n\n"
    prompt += "Search Queries and Answers:\n"
    for query, result in zip(search_queries, results):
        prompt += f"Query: {query}\nAnswer: {result.data}\n\n"
    print(f"Creating prompt took {time.time() - prompt_creation_start_time} seconds")

    # getting a final response
    final_response_start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_model=Answer,
        messages=[
            {
                "role": "user",
                "content": f"Using the data below. Answer the question: '\n{search_input}' \n{prompt}",
            },
        ]
    )
    print(f"Getting final response took {time.time() - final_response_start_time} seconds")

    # Update the LLMTask with the final answer
    current_llm_task.answer = response.answer
    current_llm_task.save()

    total_time = time.time() - start_time  # Total time of the task
    print(f"Total task time: {total_time} seconds")

    return response.answer
