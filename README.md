## Business internal llm voice call to get answers and storage of those interactions in postgresql database

# Pre-requirements
- install LMStudio
- install Ollama (will be done through the requirement file)
- install lanchain (same will be done with requirement file install)
- install postgresql
- install pgvector postgresql extension (so activate it as well  `CREATE EXTENTION vector;` 'pgvector' or 'vector', mine worked with 'vector')

# requirements
- create a python virtual environement 
```python 
python3 -m venv <MEANINGFUL_VIRTUAL_ENVIRONMENT_NAME> 
```
```bash
source <YOUR_VIRTUAL_ENVIRONMENT_NAME>/bin/activate
```
```python
pip install -r <THE_REQUIREMENT_FILE>.txt
# then go have a coffee or tea or walk a bit for you blood circulation 
```
- Linux Ubuntu-22.04 (worked fine for me) or wsl2 with X11 Xserver maybe for UI (LMStudio or app html page if we develop it further)
- install requirements and fix dependencies issues if there is any, at the moment of writing this README it was fine just like that (Feb 2024)
- Make sure to test your mic online to have your voice transcribed

# improvememts to do
- Try to get better models opensource running locally (Mistral:7B is used here for Ollama and TheBloke Mistral7b for LMStudio)
- Get better voice transcriber
- Get better voice output as the one here is bit tired, they were only male voices so I used a trick adding options for the voice to sound feminine
- Work on the improvement of the RAG like embedding for a more performant way to store the data and chunk it in a clever way.

# issues
- Tried to use Lantern for embeddings as well but the dimension size of ollama embedding endpoint is 4096 while Lantern is set at 1536 and supported range is 0 to 2000. PGVector doesn't mind and worked fine so I suggets you to use that one.
