from validate import validate

if __name__ == "__main__":
    from helper_functions import readJSONFile

    data = readJSONFile("assets/optimized.json")
    validate(data=data)
    print("Validation succeeded") # When the data is invalid this will not be reached
