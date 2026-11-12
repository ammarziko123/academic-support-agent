\# Academic Support Agent



An AI-powered Academic Support Assistant built using Retrieval-Augmented Generation (RAG), FAISS, Sentence Transformers, Groq, and Streamlit.



The system helps students get answers to academic questions using a predefined knowledge base and provides tools for grade calculation, assignment deadline lookup, and support ticket creation.



\## Features



\- \*\*RAG-based Question Answering:\*\* Retrieves relevant information from academic documents.

\- \*\*Semantic Search:\*\* Uses Sentence Transformers and FAISS.

\- \*\*AI Agent:\*\* Uses Groq LLM with tool calling.

\- \*\*Grade Calculator:\*\* Calculates student grades and percentages.

\- \*\*Deadline Lookup:\*\* Retrieves assignment dates and submission formats.

\- \*\*Support Tickets:\*\* Creates and stores student support tickets.

\- \*\*Streamlit Interface:\*\* Provides an interactive chat interface.

\- \*\*Evaluation:\*\* Includes tests for RAG, agent behavior, tools, tickets, and deadlines.



\## Tech Stack



\- Python

\- Streamlit

\- FAISS

\- Sentence Transformers

\- Groq API

\- NumPy

\- python-dotenv



\## Project Structure



```text

academic-support-agent/

├── knowledge\_base/

├── src/

├── data/

├── evaluation/

├── app.py

├── check\_knowledge\_base.py

├── requirements.txt

└── README.md

```



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/YOUR\_USERNAME/academic-support-agent.git

cd academic-support-agent

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



\### 3. Install dependencies



```powershell

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



\### 4. Configure the API key



Create a `.env` file in the project root:



```env

GROQ\_API\_KEY=your\_groq\_api\_key

```



Replace the placeholder with your own Groq API key. Never upload your `.env` file.



\## Build the Knowledge Base



```powershell

.\\.venv\\Scripts\\python.exe src\\rag\_pipeline.py

```



This builds the FAISS knowledge index and runs sample semantic-search questions.



\## Run the Application



```powershell

.\\.venv\\Scripts\\python.exe -m streamlit run app.py

```



\## Run Evaluation Tests



```powershell

.\\.venv\\Scripts\\python.exe evaluation\\evaluate\_rag.py

.\\.venv\\Scripts\\python.exe evaluation\\evaluate\_agent.py

.\\.venv\\Scripts\\python.exe evaluation\\evaluate\_tools.py

.\\.venv\\Scripts\\python.exe evaluation\\evaluate\_tickets.py

.\\.venv\\Scripts\\python.exe evaluation\\evaluate\_deadlines.py

```



The project achieved \*\*29/29 passing test cases (100%)\*\* across the defined evaluation scripts. This does not guarantee correctness for every possible input.



\## Knowledge Base



The knowledge base contains:



\- Course catalog

\- Attendance policy

\- Assignment policy

\- Academic calendar

\- Student FAQs



\*\*Note:\*\* The academy information and academic records are fictional sample data created for demonstration and testing purposes.



\## Security



\- API keys and environment variables are excluded using `.gitignore`.

\- The local virtual environment is excluded.

\- Generated support ticket data is excluded to avoid publishing student information.



\## Future Improvements



\- Add user authentication.

\- Improve conversation memory.

\- Add more academic tools.

\- Expand the evaluation dataset.

\- Deploy the application online.



\## Author



Developed as an AI project demonstrating RAG, semantic search, LLM tool calling, and Streamlit application development.

