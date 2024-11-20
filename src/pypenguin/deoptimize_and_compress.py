import os, shutil
import urllib.parse

from pypenguin.deoptimize import deoptimizeProject

from pypenguin.helper_functions import readJSONFile, writeJSONFile, pp

from pypenguin.database import defaultCostumeFilePath

def deoptimizeAndCompressProject(
    optimizedProjectDirectory: str,
    projectFilePath          : str,
    temporaryDirectory       : str,
    writeDebugFiles          : bool = False,
):
    # Read the optimized project.json
    optimizedData = readJSONFile(
        os.path.join(optimizedProjectDirectory, "project.json")
    )
    # Deoptimize the project data
    deoptimizedData = deoptimizeProject(
        projectData=optimizedData,
    )
    if writeDebugFiles:
        writeJSONFile("temp3.json", data=deoptimizedData)
    # Make sure the temporary directory exists
    os.makedirs(temporaryDirectory, exist_ok=True)
    
    # Write the deoptimized project.json
    writeJSONFile(
        filePath=os.path.join(temporaryDirectory, "project.json"),
        data=deoptimizedData,
    )

    # Reorganize Assets
    for i, sprite in enumerate(optimizedData["sprites"]):
        deoptimizedSprite = deoptimizedData["targets"][i]

        # Encode the sprite name
        if sprite["isStage"]:
            encodedSpriteName = "#Stage"
        else:
            encodedSpriteName = urllib.parse.quote(sprite["name"])
        
        pp(deoptimizedSprite["costumes"])
        # Copy and rename costumes
        for j, costume in enumerate(deoptimizedSprite["costumes"]):
            #pp(costume)
            oldCostumeName                        = costume["md5ext"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            if costume.get("isDefault") == True:
                srcPath = defaultCostumeFilePath
            else:
                srcPath = os.path.join(
                    optimizedProjectDirectory, 
                    encodedSpriteName, 
                    "costumes", 
                    encodedCostumeName
                )
            shutil.copy(
                src=srcPath,
                dst=os.path.join(temporaryDirectory, oldCostumeName),
            )
            print("-->", oldCostumeName, encodedCostumeName, srcPath)
        
        # Copy and rename sounds
        for j, sound in enumerate(deoptimizedSprite["sounds"]):
            #pp(sound)
            oldSoundName                        = sound["md5ext"]
            encodedSoundName = urllib.parse.quote(sound["name"] + "." + sound["dataFormat"])
            srcPath = os.path.join(
                optimizedProjectDirectory, 
                encodedSpriteName, 
                "sounds", 
                encodedSoundName
            )
            shutil.copy(
                src=srcPath,
                dst=os.path.join(temporaryDirectory, oldSoundName),
            )
            print("-->", oldSoundName, encodedSoundName, srcPath)
        """for costume in sprite["sounds"]:
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
            )"""

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
