import uvicorn

from api import ImportApi
from PipelineManager import PipelineManager
from environment import EnvironmentVariables as Ev

# Instantiate EnvironmentVariables class for future use. Environment constants cannot be accessed without this

Ev()


def run_api():
    uvicorn.run(ImportApi.app, host="0.0.0.0")

    """
    This function processes the stored articles and manuals from Grundfos and Nordjyske.
    This includes the extraction of data from the .json files, the lemmatization and wordcount,
    uploading data to the database.
    
    :param content: json file
    :return: No return
    """


if __name__ == "__main__":
    PipelineManager().run_pipeline()
