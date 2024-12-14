# Coursera Agent : Generate PDF using RAG with OpenAPI + Chroma Vector Database


## Setup Coursera Agent Python Environment

1. Install python packages
>Recommended to use `uv` to install python packages in a virtual environment.
```
uv python pin 3.12  
uv venv
uv pip install -r requirements.txt
```
2. Create `input`, `output` and `prompts` directories
```
mkdir input output prompts
```
3. Create `.env` file with OpenAI API Key and other configurations
```
OPENAI_API_KEY=sk-xxxx
```
4. Start Chroma Vector Database
```
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

Check current settings
```
uv run python main.py check <course-name>
```

Get course information
```
uv run python main.py info <course-name>
```

Load course materials
```
uv run python main.py load <course-name>
```

Generate PDF
```
uv run python main.py generate <course-name>
```