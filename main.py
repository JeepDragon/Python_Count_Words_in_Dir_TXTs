import sys #Module used for taking in arguments if running from the command prompt
import os #Module used for searching files and directory structures
import re #Module used for using regular expressions to find words in a file's contents

def getFilePaths(directory):
    """
    Gets a list of paths to all .txt files from a given directory.
    :param directory: The directory in which to search for .txt files
    :type directory: str
    :return: A list of paths to .txt files
    :rtype: list
    """

    #Stores a list of .txt file paths to be returned.
    list_file_paths = []
    #Loop through the directory information.
    for dir_path, dir_names, file_names in os.walk(directory):
        #Loop through each file name in the list of file names.
        for file_name in file_names:
            #Only allow .txt files to be searched.
            if os.path.splitext(file_name)[1].lower() == ".txt":
                #Add the found .txt file with its path to be returned.
                list_file_paths.append(os.path.join(dir_path, file_name))
    #Return the list of paths to .txt files.
    return list_file_paths

#Takes in a given path to
def getWordCounts(file_path, words_list, words_dict):
    """
    Gets a dictionary of given words and their found counts from a given text file.
    :param file_path: A path to a text file
    :type file_path: str
    :param words_list: A list of words as strings to search for in the file_path
    :type words_list: list
    :param words_dict: A current dictionary of words and their found counts
    :type words_dict: dict
    :return: An updated dictionary of words and their found counts from the given words_dict
    :rtype: dict
    """

    #Save the given dictionary of words and their counts into a separate return. Might not be necessary.
    returned_words_dict = words_dict
    file_contents = ""
    #Read all of the text from the file and store it in file_contents
    with open(file_path, encoding='utf-8') as file:
        file_contents = file.read()

    #Loop through each word in the given list of words
    for word in words_list:
        #Set up the pattern that makes sure it's searching for whole words instead of parts of other words.
        pattern = r"\b" + re.escape(word) + r"\b"
        #Get the number of times the given word was found in the file's contents
        word_count = len(re.findall(pattern, file_contents, re.IGNORECASE))
        #Update the dictionary with the word as a key and the word count as its value.
        if returned_words_dict.get(word) is None:
            #If the dictionary doesn't have the word as a key yet,
            # create it with the current cound found
            returned_words_dict[word] = word_count
        else:
            #If the dictionary already has the word as a key,
            # add the word count to its corrent cound it the dictionary
            returned_words_dict[word] = returned_words_dict.get(word) + word_count
    #Return the dictionary containing words as keys and their word counts as their values.
    return returned_words_dict

def getSearchResult(list_of_files, list_of_words):
    """
    Gets a dictionary of words and their found counts from a given list of .txt files and a list of words
    :param list_of_files: A list of paths to .txt files
    :type list_of_files: list
    :param list_of_words: A list of words as strings to search for in the list_of_files
    :type list_of_words: list
    :return: A dictionary of words and their found counts
    :rtype: dict
    """

    #The dictionary of words and their counts that will be built and returned.
    words_dict = {}
    #Loop through each path to a .txt file from the list of file paths
    for file_path in list_of_files:
        #Update the dictionary to be returned
        words_dict = getWordCounts(file_path, list_of_words, words_dict)
    #Return the dictionary containing words as keys and their word counts as their values.
    return words_dict


#Switch to the project_files folder under this repository
os.chdir("project_files")

#Get the current working directory
directory_containing_files = os.getcwd()

#Holds the list of words to search in the .txt files.
#If you run this from the command line and provide any words as arguments,
# these default words will be replaced.
words_to_aggregate = ["this", "Michael", "running"]

if len(sys.argv) <= 1:
    #Without arguments, we're assuming that you ran this main.py file through a regular interpreter
    # instead of from a command line.
    print("Try running program in command prompt or terminal and passing it in a path and words to search separated by spaces.")
    print("Using DEFAULT for the first argument means to use the default project directory for search.")
    print("Example: python main.py DEFAULT hello couple day")
    print("Example: python main.py \"C:\\Temp\" hello couple day")
else:
    #We're assuming here that you ran this main.py file from the command line.
    if sys.argv[1].upper() != "DEFAULT":
        #If the first parameter is the word DEFAULT, it will use the current working directory to search .txt files.
        #Otherwise, the first parameter should be a path to a directory that contains .txt files
        #Switch the working directory to whatever the first command line argument was.
        os.chdir(sys.argv[1])
        #Get the current working directory
        directory_containing_files = os.getcwd()
    if len(sys.argv) >= 3:
        #Under this condition, we know that you have given at least one word in the command line arguments.
        #Replace the default list of words with the ones in the command line parameters.
        words_to_aggregate = [word for word in sys.argv[2:]]

#Print the search results.
print("Search results:")
print(getSearchResult(getFilePaths(directory_containing_files), words_to_aggregate))
