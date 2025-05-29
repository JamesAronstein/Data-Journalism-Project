#data
#data  
#data 



#I cut out cemetery and airport neighborhoods bc had outlier values, also cut out geographic area number code (number for each borough) and NTA code (the BX01)

#do a json with the data for each borough by aggregating the data for each borough

#then do a new json with 5 keys in the dict, one for each borough, with each neighborhood and its data 

import json

f1 = open("data_cleansed.csv", "r")
lines = f1.readlines()
#print (lines)

#print (lines[0][0])


####GET DATA INTO LISTS FOR EACH ROW

data_list= []

#print (lines)
for row_i in range (len (lines)):
    #print (lines[row_i])
    row_list = []
    start = 0
    comma_count = 0
    for char_i in range (len(lines[row_i])):
        #print (lines)

        if comma_count < 5:
            if lines[row_i][char_i] == ",":

                comma_count+=1
                s = ""
                s+=lines[row_i][start: char_i]
                row_list.append(s)
                start = char_i+1
        else:
            if char_i == len(lines[row_i]) - 1:
                s= ""
                s+=lines[row_i][start: char_i]
                row_list.append(s)
        
    data_list.append(row_list)

#print (data_list)


boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

borough_aggs = {}

for b in boroughs:
    old_pop = 0
    new_pop = 0
    borough_aggs[b] = []
    for row_i in range (1, len(data_list)):
        if data_list[row_i][0] == b:
            old_pop += int (data_list[row_i][2])
            new_pop += int (data_list[row_i][3])
   
    pop_change = new_pop - old_pop
    percent_change = (pop_change/old_pop)*100 

    borough_aggs[b] = [old_pop, new_pop, pop_change, percent_change]

print (borough_aggs)

f1.close()

f2 = open("data.json", "w")
json.dump(borough_aggs, f2, indent = 4)

f2.close()
    