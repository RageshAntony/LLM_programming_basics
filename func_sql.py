import collections
import itertools
import sqlite3

import openai
import json
from colorama import Fore
from tabulate import tabulate


def dictfetchall(cursor, fet_rows):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in fet_rows]


def run_query(query: str) -> str:
    # Connect to the database
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect( './assets/data.sqlite' )
        cursor = conn.cursor()

        # Execute the SELECT query
        cursor.execute(query)
        rows = cursor.fetchall()
        # Fetch all rows from the result set

        # Get column names
        column_names = [column[0] for column in cursor.description]
        user_list = []
        # Prepare the data as a list of lists
        table_data = []
        for row in rows:
            table_data.append(list(row))

        # Converting data into json

        # Print the result as a table
        print(tabulate(table_data, headers=column_names, tablefmt="grid"))
        results = dictfetchall(cursor, rows)
        json_results: str = json.dumps(results, default=str)
        # Close the cursor and connection
        cursor.close()
        conn.close()
        return json_results

    except sqlite3.Error as error:
        print("Error connecting to MySQL database:", error)


def query_details(query: str) -> str:
    print(query)
    return run_query(query)


# Step 1, send model the user query and what functions it has access to
def run_conversation():
    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY
    guide: str = open('./assets/query.sql', "r").read()
    functions = [
        {
            "name": "query_details",
            "description": "Create an apt SQL query for a given human language query. Return the SQL query only",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Generated SQL Query",
                    }
                },
                "required": ["query"],
            },
        }
    ]
    query_desc = "Create an apt SQL query for the given human language query. For the tables created with CREATE statements like :\n\n" + guide + "\n\n Refer the tables' comment also. Return the SQL query only.  \n\n\n "

    while True:
        human_query = input(" > ")
        question = "Human: \n\n" + human_query
        print("... getting data...")
        payload = query_desc + question
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[{"role": "user", "content": payload}],
            functions=functions,
            function_call="auto",
        )

        message = response["choices"][0]["message"]
        # print(Fore.YELLOW + json.dumps(message))

        # Step 2, check if the model wants to call a function
        if message.get("function_call"):
            function_name = message["function_call"]["name"]

            if function_name == "query_details":
                arguments = json.loads(message["function_call"]["arguments"])
                # print(Fore.GREEN + json.dumps(arguments))
                # Step 3, call the function
                # Note: the JSON response from the model may not be valid JSON
                function_response = query_details(
                    query=arguments["query"]
                )
                print("\n\n... formatting table...\n\n")
                print(human_query)
                print(function_response)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {"role": "system",
                         "content": "You are a  bot which converts JSON  from user to human language format"},
                        {"role": "user", "content": human_query},
                        {"role": "function", "name": "query_details", "content": function_response}
                    ],
                    functions=functions,
                    function_call="auto",
                )

                print( response["choices"][0]["message"]['content'])


if __name__ == '__main__':
    run_conversation()
