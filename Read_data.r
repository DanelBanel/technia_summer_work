library(rjson)

#data_path = "C:\\summerwork\\_ELK_DATA_LOGS\\MCS\\srv14220\\1\\"

#MCS
data_1 = fromJSON(file = "C:\\summerwork\\_ELK_DATA_LOGS\\MCS\\srv14220\\1\\Castor-3dspace-plmprod.2018-08-22.json")
print(data_1)
data_2 = fromJSON(file = "C:\\summerwork\\_ELK_DATA_LOGS\\MCS\\srv14220\\1\\Castor-3dspace-plmprod.2018-08-23.json")
print(data_2)

#PARTIAL_INDEXING
#D:\_ELK_DATA_LOGS.zip\_ELK_DATA_LOGS\PARTIAL_INDEXING
data_3 = fromJSON(file = "C:\\summerwork\\_ELK_DATA_LOGS\\PARTIAL_INDEXING\\Castor-indexing.plmprod.2018-08-22.json")
print(data_3)

#SEARCH
#data_4 = read.csv2("C:\\summerwork\\_ELK_DATA_LOGS\\SEARCH\\search.csv.20180903.00000")
#print(data_4[0])
#https://www.r-bloggers.com/using-colclasses-to-load-data-more-quickly-in-r/
#TODO https://stackoverflow.com/questions/13022299/specify-custom-date-format-for-colclasses-argument-in-read-table-read-csv/13022441#13022441
#setAs("character","myDate", function(from) as.Date(from, format="%d/%m/%Y") )
#För mer än bara datum? Allt som öföljer ett liknande mönster


#TODO fix inconsistencies in the data so all is not character
colCLasses_txt = c("character", "character", "character", "character", "character", "character", "character", "character", "character","character", "character", "character", "character", "character")
data_3 = read.csv("C:\\Program1\\test1_txt.csv", encoding="UTF-8", colClasses = colCLasses_txt)
data_2 = data_5$X.
colClasses_json  = c("double", "character", "character", "character", "character", "character", "logical",  "character", "list")
data_6 = read.csv("C:\\Program1\\test1_json.csv", encoding="UTF-8", colClasses = colClasses_json)
