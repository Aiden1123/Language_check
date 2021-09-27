import requests
import sys

#/////////////////////////Auxilairy functions////////////////////////

def keys_max_values(dictionary):
    max_value = max(dictionary.values())
    res = []
    for key in dictionary:
        if dictionary[key]==max_value:
            res.append(key)
    return res

#/////////////////////////Main////////////////////////////////////

input_string = """Please use at least 6 words otherwise it is going to freak out"""         #Input string here to check its language

unwanted_characters = """,./;'\[]!@#"$%^&*()_+-={}|:?><"""                                  #Characters that are going to be omitted

for char in unwanted_characters:                                                            #Omitting characters
    input_string = input_string.replace(char,"")

input_string = input_string.casefold()                                                      #Changle all words to lowercase

input_words = input_string.split(" ")
print(input_words)

#print(response.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"])
#print(type(response.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]))

langs_counts = {}

for word in input_words:

    response =requests.get("https://en.wiktionary.org/w/api.php?action=query&format=json&prop=revisions&titles=" +    #get info from wiktionary
                            word + "&formatversion=2&rvprop=content&rvslots=*")
    
    if response.status_code  >= 300:                    #Handle errors
        print("an error has occured: " + str(response.status_code))
        print(response.json())
        sys.exit(1)

    if not "query" in response.json():
        continue   
    
    if "missing" in response.json()["query"]["pages"][0]:    #if word isn't found try to find capitalised or upper case version
        response =requests.get("https://en.wiktionary.org/w/api.php?action=query&format=json&prop=revisions&titles=" + word.capitalize() + "&formatversion=2&rvprop=content&rvslots=*")

        if response.status_code  >= 300:                    
            print("an error has occured: " + str(response.status_code))
            print(response.json())
            sys.exit(1)

        if "missing" in response.json()["query"]["pages"][0]:
            response =requests.get("https://en.wiktionary.org/w/api.php?action=query&format=json&prop=revisions&titles=" + word.upper() + "&formatversion=2&rvprop=content&rvslots=*")

            if response.status_code  >= 300:                    
                print("an error has occured: " + str(response.status_code))
                print(response.json())
                sys.exit(1)

            if "missing" in response.json()["query"]["pages"][0]:       #if word couldn't be found then continue
                continue

    list = response.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"].split("\n")         #find languages matching for this word
    
    for x in list:
        if x.startswith("==") and x[2].isalpha():
            x = x[2:-2]
            if x in langs_counts:                                                                               #update dictionary with languages
                langs_counts[x]+=1
            else:
                langs_counts[x]=1

if len(langs_counts) == 0:                                                      #display results
    print("no words were found")
    sys.exit(0)

results = keys_max_values(langs_counts)


if len(results) == 1:
    print("The dominant language seems to be: " + results[0])
else:
   print("The language is any of the following: " + str(results))