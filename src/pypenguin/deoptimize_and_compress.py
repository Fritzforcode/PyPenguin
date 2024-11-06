import os, shutil
import urllib.parse

from deoptimize import deoptimizeProject

from helper_functions import readJSONFile, writeJSONFile

def deoptimizeAndCompressProject(
    optimizedProjectDirectory: str,
    projectFilePath: str,
    temporaryDirectory: str,
):
    # Read the optimized project.json
    optimizedData = readJSONFile(
        os.path.join(optimizedProjectDirectory, "project.json")
    )
    # Deoptimize the project data
    deoptimizedData = deoptimizeProject(
        projectData=optimizedData,
    )
    #writeJSONFile("temp3.json", data=deoptimizedData)
    # Make sure the temporary directory exists
    os.makedirs(temporaryDirectory, exist_ok=True)

    # Write the deoptimized project.json
    writeJSONFile(
        filePath=os.path.join(temporaryDirectory, "project.json"),
        data=deoptimizedData,
    )

    # Reorganize Assets
    for sprite in optimizedData["sprites"]:
        # Encode the sprite name
        if sprite["isStage"]:
            encodedSpriteName = "#Stage"
        else:
            encodedSpriteName = urllib.parse.quote(sprite["name"])
        
        # Copy and rename costumes
        for costume in sprite["costumes"]:
            oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            shutil.copy(
                src=os.path.join(
                    optimizedProjectDirectory, 
                    encodedSpriteName, 
                    "costumes", 
                    encodedCostumeName
                ),
                dst=os.path.join(temporaryDirectory, oldCostumeName),
            )
        
        # Copy and rename sounds
        for costume in sprite["sounds"]:
            oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            shutil.copy(
                src=os.path.join(
                    optimizedProjectDirectory, 
                    encodedSpriteName, 
                    "sounds", 
                    encodedCostumeName
                ),
                dst=os.path.join(temporaryDirectory, oldCostumeName),
            )

    # Make sure projectFilePath does not exist
    if os.path.exists(projectFilePath):
        os.remove(projectFilePath)

    # Compress the temporary directory into a zip file
    shutil.make_archive(
        os.path.splitext(projectFilePath)[0],
        "zip",
        temporaryDirectory,
    )

    # Change its file extension to .pmp
    os.rename(
        os.path.splitext(projectFilePath)[0] + ".zip",
        projectFilePath,
    )

    # Remove the temporary dir
    shutil.rmtree(temporaryDirectory)

if __name__ == "__main__":
    deoptimizeAndCompressProject(
        projectFilePath           = "assets/studies/example.pmp",
        optimizedProjectDirectory = "optimizedProject/",
        temporaryDirectory        = "temporary/",
    )
