# The Retriever Squad RAG

## Installation 
1. Install requirements: `pip install -r requirements.txt`
2. The application uses python `venv` to create virtual environment

## Environment setup

More or less all of the setup will be configured through the `.env` file

1. DATA_PATH should be the path of the project dataset. An example is given in the `.env` file
2. We are running milvus for vector embedding. To run milvus, simply run the following
```bash
docker-compose up
```
After which you should get the milvus and phoenix running in docker.

### Running
1. To activate the environment, run `source venv/bin/activate`
2. Run the streamlit app: `streamlit run app.py`

This will start up the app on `localhost:8501` where you will find a simple search bar. Before you start editing, you'll notice that the app will only show you instructions on what to edit.

Example `.env`

```
EMBEDDING_MODEL=nomic-embed-text
GENERATIVE_MODEL=llama3.1
```


