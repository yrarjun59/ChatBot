import time

from ai21 import AI21Client

API_KEY = "s6MU7eAiu4MiFicLe9dAdHa1fuZNnsGJ"

client = AI21Client(
    api_key=API_KEY
)

def get_llm_response(user_query, document_content):

    prompt = f"User: {user_query}\nDocument: {document_content}\n"

    # Read guidelines from prompts.txt
    with open('prompts.txt', 'r', encoding='utf-8') as file:
        guidelines = ""
        line = file.readline()

        while line:
            guidelines += line
            line = file.readline()

    final_prompt = f"""User Inquiry: '{user_query}'. Here's your guidance for providing user-friendly responses related to books:

    {prompt}

    📚 Guidelines for Responses:
    ""{guidelines}""

    How to Respond:
    - Craft concise and engaging book recommendations based on different genres.
    - Provide key details about specific books, including the author, genre, and a brief summary.
    - Tailor responses to user preferences, considering their previous interactions.
    - Encourage interactive queries by asking open-ended questions to prompt further discussion.
    - Organize multiple recommendations in a clear and structured manner.
    - Acknowledge and use information about user favorites to enhance personalization.
    - Apologize and explain limitations when faced with queries outside the book-related context.
    - Prompt users to ask follow-up questions or provide additional details for a personalized experience.
    - Express enthusiasm about books and the user's literary interests.

    Remember, our primary focus is on books. Create an engaging and positive interaction experience for users exploring the world of literature! Ready to assist with book-related inquiries?"""

    start_time = time.time()
    
    # Generate response from the LLM
    response = client.completion.create(
        model="j2-ultra",
        prompt=final_prompt,
        temperature=0.7,
        max_tokens=100,
    )

    end_time = time.time()
    time_taken_seconds = round(end_time - start_time, 2)
    time_taken_minutes = round(time_taken_seconds / 60, 2)

    # Limit the response to max_characters
    completion = response.completions[0].data.text.strip()


    if time_taken_minutes >= 1:
        time_message = f"Completed in {time_taken_minutes} minutes"
    else:
        time_message = f"Completed in {time_taken_seconds} seconds"

  
    return completion,time_message

with open('documents.txt', 'r', encoding='utf-8') as file:
    document_content = file.read()


def is_harmful_input(user_query):
    harmful_keywords = ['bomb', 'illegal content', 'harmful activity', 'other_harmful_keyword', '...']  
    return any(keyword in user_query.lower() for keyword in harmful_keywords)

first_time = True  

def get_user_input():
    global first_time 
    if first_time:
        user_query = input("I am here to help you. Ask me:\n")
        first_time = False  
    else:
        user_query = input()  
    return user_query

def main():
    while True:
        user_query = get_user_input()

        # Check for stop command
        if user_query.lower() in ['stop', 'exit', 'quit']:
            print("Chatbot stopping. Goodbye!")
            break


        if is_harmful_input(user_query):
            print("I'm sorry, but I cannot provide assistance or guidance on harmful or illegal content. My purpose is to offer helpful and responsible information within ethical and legal boundaries. Feel free to ask non-controversial questions or make requests within those limits.")
            continue 

        llm_response = get_llm_response(user_query, document_content)
        response, time = llm_response
        print(response)
        print(time)

if __name__ == "__main__":
    main()
