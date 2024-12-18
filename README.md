# Coursera Agent : Generate PDF using RAG with [LangChain](https://python.langchain.com/docs/introduction/) + [Chroma Vector Database](https://docs.trychroma.com/)


## Setup Coursera Agent Python Environment

1. Install python packages
>Recommended to use [uv](https://docs.astral.sh/uv/) to install python packages in a virtual environment.
```bash
uv python pin 3.12  
uv venv
uv pip install -r requirements.txt
```
2. Create `input`, `output` directories and overwrite `prompts` directory
```bash
mkdir input output
cp -r examples_prompts prompts
# overwrite your own prompts
```
3. Create `.env` file with OpenAI API Key and other configurations
```bash
OPENAI_API_KEY=sk-xxxx
```
4. Start Chroma Vector Database
```bash
docker compose up -d
```

## Download Coursera Materials

Note:
- Get `<cauth>` from browser cookies.
- Should **download in `input` directory**.
```bash
# If not enter `input` directory
cd input
# List all courses
uv run coursera-helper --cauth <cauth> --list-course
# Download course materials
# will download quizzes, assignments, lecture notes, and video transcripts
# only download subtitles in English
uv run coursera-helper --cauth <cauth> --download-quizzes --about --subtitle-language en <course-name>
```
> Reference [Coursera Helper](https://github.com/csyezheng/coursera-helper)


## Usage

Help
```
usage: main.py [-h] [-v] [-q] [-i] {check,info,load,delete,generate} ...
main.py: error: the following arguments are required: verb
```

1. Check current settings is valid
```
uv run python main.py check <course-name>
```

2. Get course information, will list all materials to be loaded
```
uv run python main.py info <course-name>
```

3. Load course materials into Chroma Vector Database
```
uv run python main.py load <course-name>
```

4. Generate PDF
> [!NOTE]  
> Should install [marp-cli](https://github.com/marp-team/marp-cli) to generate PDF from markdown.
```
uv run python main.py generate <course-name>
```