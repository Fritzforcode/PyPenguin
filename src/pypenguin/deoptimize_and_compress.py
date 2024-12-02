import os, shutil
import urllib.parse

from pypenguin.deoptimize import deoptimizeProject

from pypenguin.helper_functions import readJSONFile, writeJSONFile, insureCorrectPath

from pypenguin.database import defaultCostumeFilePath

def deoptimizeAndCompressProject(
    optimizedProjectDir: str,
    projectFilePath    : str,
    temporaryDir       : str,
    writeDebugFiles    : bool = False,
):
    optimizedProjectDir = insureCorrectPath(optimizedProjectDir,    "PyPenguin")
    projectFilePath     = insureCorrectPath(projectFilePath,        "PyPenguin")
    temporaryDir        = insureCorrectPath(temporaryDir,           "PyPenguin")
    temp3FilePath       = insureCorrectPath("temp3.json",           "PyPenguin")
    defCostumeFilePath  = insureCorrectPath(defaultCostumeFilePath, "PyPenguin")
    
    # Read the optimized project.json
    optimizedData = readJSONFile(
        os.path.join(optimizedProjectDir, "project.json")
    )
    # Deoptimize the project data
    deoptimizedData = deoptimizeProject(
        projectData=optimizedData,
    )
    if writeDebugFiles:
        writeJSONFile(temp3FilePath, data=deoptimizedData)
    # Make sure the temporary Dir exists
    os.makedirs(temporaryDir, exist_ok=True)
    
    # Write the deoptimized project.json
    writeJSONFile(
        filePath=os.path.join(temporaryDir, "project.json"),
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
        
        # Copy and rename costumes
        for j, costume in enumerate(deoptimizedSprite["costumes"]):
            oldCostumeName                        = costume["md5ext"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            if costume.get("isDefault") == True:
                srcPath = defCostumeFilePath
            else:
                srcPath = os.path.join(
                    optimizedProjectDir, 
                    encodedSpriteName, 
                    "costumes", 
                    encodedCostumeName
                )
            shutil.copy(
                src=srcPath,
                dst=os.path.join(temporaryDir, oldCostumeName),
            )
        
        # Copy and rename sounds
        for j, sound in enumerate(deoptimizedSprite["sounds"]):
            oldSoundName                        = sound["md5ext"]
            encodedSoundName = urllib.parse.quote(sound["name"] + "." + sound["dataFormat"])
            srcPath = os.path.join(
                optimizedProjectDir, 
                encodedSpriteName, 
                "sounds", 
                encodedSoundName
            )
            shutil.copy(
                src=srcPath,
                dst=os.path.join(temporaryDir, oldSoundName),
            )
        """for costume in sprite["sounds"]:
            oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            shutil.copy(
                src=os.path.join(
                    optimizedProjectDir, 
                    encodedSpriteName, 
                    "sounds", 
                    encodedCostumeName
                ),
                dst=os.path.join(temporaryDir, oldCostumeName),
            )"""

    # Make sure projectFilePath does not exist
    if os.path.exists(projectFilePath):
        os.remove(projectFilePath)

    # Compress the temporary Dir into a zip file
    shutil.make_archive(
        os.path.splitext(projectFilePath)[0],
        "zip",
        temporaryDir,
    )
    print("created", projectFilePath)

    # Change its file extension to .pmp
    os.rename(
        os.path.splitext(projectFilePath)[0] + ".zip",
        projectFilePath,
    )

    # Remove the temporary dir
    shutil.rmtree(temporaryDir)

if __name__ == "__main__":
    deoptimizeAndCompressProject(
        projectFilePath           = "assets/studies/example.pmp",
        optimizedProjectDir = "optimizedProject/",
        temporaryDir        = "temporary/",
    )
