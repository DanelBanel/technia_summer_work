import json
import numpy as np
import os
import re
import csv
from collections import defaultdict
path = "C:\summerwork\_ELK_DATA_LOGS\MCS\srv14220\\1\\"
write_path = "C:\Program1\\"
filename_json = path + "Castor-3dspace-plmprod.2018-08-22.json"
filename_txt = path + "plmprod-1.access.2018-08-22.log"
suffix_json = ".json" #Used in createListFromFile
suffix_txt = ".log"

'''            Help functions             '''

def createListFromFolder(folder_path, suffix):
    '''
    Creates a list from all rows in the files in a folder (.json or .log)
    
    Input: 
        folder_path: Path to folder with files
        suffix: Read .log or .json files?
    Output:
        list with all unseperated information
    '''
    file_name_array = getFileNamesFromFolder(folder_path)
    complete_data_txt = createListFromFile(folder_path+file_name_array[0], suffix)
    for file_idx in range(1,len(file_name_array)):
        addListFromFileName(complete_data_txt, folder_path+file_name_array[file_idx], suffix)
    return complete_data_txt
    

def createListFromFile(filename,suffix):
    '''
        Creates a list from all rows in a file (.json or .log)
    Input:
        filename: Path to file + filename
        suffix: Read .log or .json files?
    Output:
        list with all unseperated information
    '''
    array = []    
    try: 
        with open(filename, 'rt', encoding="utf8") as f:
            if filename.endswith(suffix_txt) and suffix == suffix_txt:
                 array = f.readlines() 
                 print("Reading .log: ", filename)
            elif filename.endswith(suffix_json) and suffix == suffix_json:
                 array = [json.loads(line) for line in f]
                 print("Reading .json: ", filename)
    except Exception as e:
        print("Failed to load. May be corrupt file or no ", suffix, "-file. Exception: ", e)     
    return array

def addListFromFileName(l, filename, suffix):
    '''
        Extends existing list with new information from new file
    Input:
        l: existing list
        filename: Path to file + filename
        suffix: Read .log or .json files?
    Output:
        extended list
    '''
    return l.extend(createListFromFile(filename, suffix))

def getAllKeys(json_object):
    '''
        Returns a list with all keys from a json_object
    Input:
        json_object: dict
    Output:
        A list of all keys in dict
        
    '''
    keys = []
    for key in json_object:
        keys.append(key)
    return keys

def fillAllKeyArrays(json_list):
    '''
        Fill all arrays with the appropriate information from the list of dicts
    Input:
        json_list: list of json_object
    Output:
        -
    '''
    timeMillis_array = []
    thread_array = []
    level_array = []
    loggerName_array = []
    message_array = []
    endOfBatch_array = []
    loggerFqcn_array = []
    contextMap_array = []
    keys = getAllKeys(json_list)
    for row_index in range(len(json_list)):    
        timeMillis_array.append(json_list[row_index][keys[0]])
        thread_array.append(json_list[row_index][keys[1]])
        level_array.append(json_list[row_index][keys[2]])
        loggerName_array.append(json_list[row_index][keys[3]])
        message_array.append(json_list[row_index][keys[4]])
        endOfBatch_array.append(json_list[row_index][keys[5]])
        loggerFqcn_array.append(json_list[row_index][keys[6]])
        contextMap_array.append(json_list[row_index][keys[7]])


def findAllUniqueTags(key, json_list):
    '''
        Find unique information for a key, return list
    Input:
        key: key searched for
        json_list: list of json_object
    Output:
        List of unique tags (tex. ['ERROR', 'INFO', 'WARN', 'FATAL'] for key = "level")
    '''
    filter_array = []
    unique_tags = []
    for row_index, row in enumerate(json_list):      
        if not any(filter_string in json_list[row_index][key] for filter_string in filter_array):
            unique_tags.append(json_list[row_index][key])
            filter_array.append(json_list[row_index][key])
    return unique_tags

def findAllUniqueTagsReturnArraysAsDict(key, json_list):
    '''
        Find unique information for a key, return as dict
   Input:
        key: key searched for
        json_list: list of json_object
    Output:
        Dict of unique tags 
    '''
    unique_tags = findAllUniqueTags(key, json_list)
    d = defaultdict(list)
    for row_index, row in enumerate(json_list):
        for tag in unique_tags:
            if(json_list[row_index][key] == tag):
                d[json_list[row_index][key]].append(row)
    return d
                
#Filters all element in array on a substring
def filterArrayOnSubString(list_objects, substring):
    '''
        Filter away elements in list that do not contain the substring
    '''
    list_filtered = []
    for d in list_objects:
        string_dict = json.dumps(d)
        if substring in string_dict:
            list_filtered.append(d)
    return list_filtered

def calculateAverageOfArray(array):
    '''
        Calculates average of all elements in array (used for tex. timeMillis), return average
    '''
    if (len(array) == 0):
        return 0
    return sum(array)/len(array)

#Filter timeMillis on a value and make to a new array. Done by converting to numpy-array for speed. Dont know if numpy is heavily used at Technia which is why not generally used
def filter_timeMillis(timeMillis_array,  timeMillis_filter = 1534930000000):
    '''
        Filter away elements that do no match the filter-value, return filtered list
    '''
    timeMillis_array_filtered =  np.array(timeMillis_array)[np.array(timeMillis_array) > timeMillis_filter]
    return timeMillis_array_filtered
    
def getFileNamesFromFolder(folder_path):
    '''
        Get a list of all filenames from a folderpath
    '''
    return os.listdir(folder_path)

def filterUserName(string, filter_string):
    '''
        Search if filter_string is in string    
    '''
    return re.search(filter_string, string).group(1)  

def WriteDictToCSV(csv_file, d):
    '''
        Opens a csv-file and writes the header and all lists of information to that file
    Input:
        csv_file: path to outputfile + outputfile name
        d: new information as dict
    Output:
        - 
    '''
    if len(d) != 1:
        try:
            with open(csv_file, 'w') as file:
                 writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                 writer.writerow(d.keys())
                 for idx in range(len(d[list(d.keys())[0]])):    
                     writer.writerow([d[key][idx] for key in d.keys()])
        except Exception as e:
                print("Exception", e)    
    return  

def WriteDictToOpenCSV(csv_file, d, counter):
    '''
        Takes a open csv_file and concatenates the new information to that file.
    Input:
        csv_file: open csv_file
        d: new information as dict
        counter: used to only write header-columns for the first file
    Output:
        counter: adds and return so no header is written for the second file
    '''
    if len(d) != 1:
        try:
             writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             if counter == 1:
                 counter += 1
                 writer.writerow(d.keys())
             for idx in range(len(d[list(d.keys())[0]])):    
                 writer.writerow([d[key][idx] for key in d.keys()])
        except Exception as e:
                print("Exception", e)    
    return counter

def createDictFromList(data_txt, tag_array = ["IP", "Time", "Method", "Request","Params","HTTP-type","Response", "?", "??", "Referer", "Useragent", "Username", "???"], split_c = "|"):
    '''
        Takes a list and splits it into the appropriate dict-parts using a tag_array with keys and a split_character
    
    Input:
        data_txt: List of information
        tag_array: Keys to split into, instansiated by .log files
        split_c: character to split on, instansiated as "|" from .log files
    Output:
        dict: the full dict
    '''
    d_txt = defaultdict(list)
    d_txt.fromkeys(tag_array)

    for string in data_txt:
        string_split = string.split(split_c)
        for tag_idx, tag in enumerate(tag_array):
            d_txt[tag].append(string_split[tag_idx])
    d_txt['Total'] = data_txt
    return d_txt

def filterUserNamesDict(d_txt):
    '''
         Filter data to only include data entries with a attached username 
    Input:
        d_txt: dict
    Output:
        filtered dict
    '''
    filter_string_tracking_id = "userName=(.*)&X-Atmosphere-tracking-id="
    filter_string_transport = "userName=(.*)&X-Atmosphere-Transport=close&X"
    d_txt['User'] = d_txt['Params']
    for row_idx, row in enumerate(d_txt["User"]):
        if ("-" not in d_txt["Username"][row_idx] and "/" not in d_txt["Username"][row_idx] and "." not in d_txt["Username"][row_idx]): #Filter away inconsistencies in the data such as useragent or HTTP-type
            d_txt["User"][row_idx] = d_txt["Username"][row_idx]
        else:
            if("userName=" in row and "X-Atmosphere-Transport=close&X" in row):
                d_txt["User"][row_idx]  =  filterUserName(d_txt["User"][row_idx], filter_string_transport)
            elif("userName=" in row and "X-Atmosphere-tracking-id=" in row):
                d_txt["User"][row_idx]  =  filterUserName(d_txt["User"][row_idx], filter_string_tracking_id)
    d_txt["User"] = [user for user in d_txt["User"] if '""' not in user and "?" not in user] 
    return d_txt

def getUniqueUsers(d_txt):
    '''
        Converts list to set and therefore only keep unique users, return set 
    '''
    return set(d_txt["User"])
 
'''                 .LOG CODE              '''

path = "C:\summerwork\_ELK_DATA_LOGS\MCS\srv14220\\1\\" #Path of files
write_path = "C:\Program1\\" #Path to write
filename_log = path + "plmprod-1.access.2018-08-22.log" #Only used when only reading 1 file, use createListFromFile
suffix_log = ".log" #To seperate from .log and .json
csv_file = write_path + "test1_log.csv" #Path to outputfile + outputfile name
counter = 1 #Used to only write header for the first file in folder
total = 0 #Total rows of information

'''
Takes a folder of files, writes all .log files to a csv file with the appropriate seperation of the data
'''

fout = open(csv_file, 'w') 
filenames =  getFileNamesFromFolder(path)
for filename_log in filenames:
    filename_log = path + filename_log
    #Creates a list to with all the data. Either from one file (createListFromFile) or all files in a folder (createListFromFolder)
    data_log = createListFromFile(filename_log, suffix_log)
    
    #Filter away unnecessary data, by looking at the requests made.
    filter_array = ["/3dspace/collaboration/communication", "dynaTraceMonitor", "/3dspace/tvc-action/lazy", "/3dspace/tvc-action/collabAvatar/", "/3dspace/tvc-action/collabProfilePicture/", "/servlet/MatrixXMLServlet", ]
    #print("Length before filtration", len(data_log))
    
    data_log_filtered = [row for row in data_log if not any(filter_string in row for filter_string in filter_array)]
    print("Length after filtration",len(data_log_filtered))
    data_log = data_log_filtered
    total = total + len(data_log)
    
    #Creates a dictionary from the list for easier access and filtration
    #List of all columns in .log. Taken by backwards engineering from Kabana
    tag_array = ["IP", "Time", "Method", "Request","Params","HTTP-type","Response", "?", "??", "Referer", "Useragent", "Username", "???"] 
    d_log = createDictFromList(data_log, tag_array)
    
    #Writes dict_data to a csv file
    counter = WriteDictToOpenCSV(fout,d_log, counter)
print("Total length of csv-file: ", total)
fout.close()

'''                  JSON CODE                     '''

path = "C:\summerwork\_ELK_DATA_LOGS\MCS\srv14220\\1\\" #Path of files
write_path = "C:\Program1\\" #Path to write
filename_json = path + "Castor-3dspace-plmprod.2018-08-22.json"  #Only used when only reading 1 file, use createListFromFile
suffix_json = ".json" #To seperate from .log and .json
csv_file = write_path + "test1_json.csv"#Path to outputfile + outputfile name
counter = 1 #Used to only write header for the first file in folder
total = 0 #Total rows of information

'''
Takes a folder of files, writes all .json files to a csv file with the appropriate seperation of the data
'''

fout = open(csv_file, 'w', encoding="utf8")
fieldnames = ['timeMillis', 'thread', 'level', 'loggerName', 'message', 'thrown', 'endOfBatch', 'loggerFqcn', 'contextMap']
filenames =  getFileNamesFromFolder(path)
for filename in filenames:
    filename_json = path + filename
    json_list = createListFromFile(filename_json, suffix_json)
    total = total + len(json_list)
    print("Length after filtration",len(json_list))
    if(len(json_list) != 0): 
        try:
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            if counter == 1: # only write header for the first file
                writer.writeheader()
                counter += 1
            for json_object in json_list:
                 writer.writerow(json_object)
        except Exception as e:
            print("Exception", e)
print("Total length of csv-file: ", total)
fout.close()

'''
    Example of what can be done with the different help functions
'''
'''
timeMillis_array = []
thread_array = []
level_array = []
loggerName_array = []
message_array = []
endOfBatch_array = []
loggerFqcn_array = []
contextMap_array = []
json_list = createListFromFile(filename_json, suffix_json)

##Arrays for saving all of the different json-key-information in different arrays
keys = getAllKeys(json_list)

##Fill all array e.g. timeMillis_array with corresponding values
fillAllKeyArrays(json_list)

#Filter the timeMillis_array on a number, calculate Avg min and max on the filtrated data(if filtration is done)
timeMillis_filter = 10
timeMillis_array_filtered = filter_timeMillis(timeMillis_array, timeMillis_filter)
print("Length of Timemillis before filtration: %d and after %d" % (len(timeMillis_array), len(timeMillis_array_filtered)))
print("TimeMillis: Avg - ", calculateAverageOfArray(timeMillis_array_filtered), " Min - ", min(timeMillis_array_filtered), " Max - ", max(timeMillis_array_filtered), " Difference is - ",  max(timeMillis_array_filtered)- min(timeMillis_array_filtered))

unique_tags = findAllUniqueTags('level', json_list)
#print("UNIQUE TAGS", unique_tags)

d = findAllUniqueTagsReturnArraysAsDict('level', json_list)
#print("All rows with level:INFO", d['INFO'])

substring = "HM Product Development"
d_info_filtered = filterArrayOnSubString(d['INFO'], substring)
#print("All rows with substring" ,d_info_filtered)        
'''