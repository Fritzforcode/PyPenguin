import os, shutil
import urllib.parse

from pypenguin.deoptimize import deoptimizeProject
from pypenguin.deoptimize.costumes_sounds import finalizeCostume, finalizeSound

from pypenguin.helper_functions import readJSONFile, writeJSONFile, insureCorrectPath, generateMd5, getImageSize

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
    # Make sure the temporary Dir exists
    os.makedirs(temporaryDir, exist_ok=True)

    # Reorganize Assets
    for i, sprite in enumerate(optimizedData["sprites"]):
        deoptimizedSprite = deoptimizedData["targets"][i]

        # Encode the sprite name
        if sprite["isStage"]:
            encodedSpriteName = "#Stage"
        else:
            encodedSpriteName = urllib.parse.quote(sprite["name"])
        
        # Copy and rename costumes
        newCostumes = []
        for j, costume in enumerate(deoptimizedSprite["costumes"]):
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
            md5    = generateMd5(file=srcPath)
            md5ext = md5 + "." + costume["dataFormat"]
            width, height = getImageSize(file=srcPath)
            shutil.copy(
                src=srcPath,
                dst=os.path.join(temporaryDir, md5ext),
            )
            newCostumes.append(finalizeCostume(
                data=costume, 
                md5=md5,
                md5ext=md5ext,
                width=width,
                height=height,
            ))
        
        deoptimizedSprite["costumes"] = newCostumes


        
        # Copy and rename sounds
        newSounds = []
        for j, sound in enumerate(deoptimizedSprite["sounds"]):
            encodedSoundName = urllib.parse.quote(sound["name"] + "." + sound["dataFormat"])
            srcPath = os.path.join(
                optimizedProjectDir, 
                encodedSpriteName, 
                "sounds", 
                encodedSoundName
            )
            md5    = generateMd5(file=srcPath)
            md5ext = md5 + "." + sound["dataFormat"]
            shutil.copy(
                src=srcPath,
                dst=os.path.join(temporaryDir, md5ext),
            )
            newSounds.append(finalizeSound(
                data=sound, 
                md5=md5,
                md5ext=md5ext,
            ))
        
        deoptimizedSprite["sounds"] = newSounds

    
    if writeDebugFiles:
        writeJSONFile(temp3FilePath, data=deoptimizedData)
    
    # Write the deoptimized project.json
    writeJSONFile(
        filePath=os.path.join(temporaryDir, "project.json"),
        data=deoptimizedData,
    )

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
