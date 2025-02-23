## a-link

a-link is a versatile Python application that dynamically executes submodules based on JSON input. It empowers users to specify an agent (submodule) and its parameters, offering a modular way to perform tasks like sending messages, analyzing trends, or fetching Twitter news—all with a design that’s easy to extend.

## Table of Contents

Installation (#installation)
Usage (#usage)
Features (#features)
Contributing (#contributing)
Testing (#testing)
License (#license)
Contact & Support (#contact--support)

## Installation
Get a-link up and running on your machine with these simple steps.

### Prerequisites

    Python 3.9+: Check your version with python --version.
    pip: Comes with Python, but ensure it’s updated (pip install --upgrade pip).
    Git: Required to clone the repo.

### Steps

Clone the repository:

```
git clone https://github.com/Stell0/a-link.git
cd a-link
```

#### Install dependencies:

Set up a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then install the required packages:

```
pip install -r requirements.txt
```

Configure environment variables:
Some agents need API keys. Create a .env file in the project root or set them manually:
OPENAI_API_KEY: For the trends agent.
TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET: For the news agent.
Optional: TRENDS_SEARCH_TERMS and NEWS_SEARCH_TERMS as JSON arrays (e.g., ["python", "ai"]).

## Usage

Run a-link by passing a JSON string with the agent name and its parameters via the command line.

### Basic Command

```
python a-link.py '{"agent": "message", "params": {"message": "Hello, World!"}}'
```

Output: Prints "Hello, World!" to the console and logs the action to stderr.

### Examples

Message Agent:

```
python a-link.py '{"agent": "message", "params": {"message": "Test message"}}'
```
Prints: "Test message"

Trends Agent:

```
python a-link.py '{"agent": "trends", "params": {"trends_search_terms": ["python", "ai"]}}'
```

Uses OpenAI to analyze trends. Falls back to TRENDS_SEARCH_TERMS if unspecified.

News Agent:
```
python a-link.py '{"agent": "news", "params": {"news_search_terms": ["technology", "AI"]}}'
```

Logs tweets to stderr. Defaults to NEWS_SEARCH_TERMS if not provided.

## Features

Modular Design: Add new agents by dropping a Python file into the agents folder—implement the Submodule class and you’re set!
Dynamic Execution: JSON input dictates which agent runs and how, making tasks endlessly adaptable.
API Integration: Seamlessly connects to services like OpenAI and Twitter using environment variables.
Logging: Actions and errors are logged to stderr, keeping debugging straightforward.

## Contributing

Love a-link and want to help? We’d love your input!

Open a pull request on GitHub.


## Testing
Verify a-link works as expected with these steps:

    Test the Message Agent:
    bash

python a-link.py '{"agent": "message", "params": {"message": "Test"}}'

    Should print "Test" to stdout.

Inspect Logs:

    Logs go to stderr. Capture them like this:
    bash

        python a-link.py '{"agent": "message", "params": {"message": "Test"}}' 2> logs.txt

    Test Other Agents:
        Set up API keys in your .env file, then run trends or news with relevant parameters.

## License
This project is licensed under the MIT License. See LICENSE for the full text.

## Contact & Support
Got questions or ideas? Reach out!

    Email: gentoo.stefano@gmail.com (mailto:gentoo.stefano@gmail.com)
    Issues: File a ticket on the GitHub repo
