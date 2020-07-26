import requests
import os

os.environ['API_KEY'] = 'YzroszryeoQb9n6ddUtS'
API_KEY = os.environ.get('API_KEY')
URL = 'https://www.quandl.com/api/v3/datasets/FSE/AFX_X.json?api_key='

#%% Functions
#Add all numbers together (skipping None values), then divide by the list's length.
def compute_average(input_list):
    total = 0
    for i in input_list:
        if i is None:
            continue
        total += i
    avg = total/len(input_list)
    return round(avg, 2)

#Replace NaN values with the average of the list's numeric values.
def remove_nan_values(input_list):
    avg = compute_average(input_list)
    return [i if type(i) == float else avg for i in input_list]

#Since we're only using standard types in this project, a custom-built function
#for subtracting list values from each other will be helpful.
#In this case, we will always want the smaller number subtracted from the larger.
def subtract_value_pairs(list1, list2):
    return [abs(i - j) for i,j in zip(list1, list2)]

#This function is for computing the median of a list of numbers.
def compute_median(input_list):
    sorted_list = sorted(input_list)
    list_len = len(input_list)
    #The index must be an int, so we use floored division to find the "middle" index.
    index = (list_len - 1) // 2

    #If the list length is not divisible by 2 
    #(i.e. dividing by two returns a non-zero remainder), 
    #return the index computed above.
    if (list_len % 2):
        return sorted_list[index]
    #Otherwise, take the average of the computed index and the next index.
    else:
        return (sorted_list[index] + sorted_list[index + 1])/2.0
#%% 1.
start_date = '2017-01-01'
end_date = '2017-12-31'

#Request data from the Franfurt Stock Exchange for the whole year of 2017.
r = requests.get(URL + API_KEY + "&start_date=2017-01-01&end_date=2017-12-31")
json_string = r.json()
#%% 2.

#Unpack the JSON string to find the column names and data for this dataset.
json_dict = dict(json_string)
json_dict = json_dict['dataset']
col_names = json_dict['column_names']
data = json_dict['data']

#Pivot the data, originally organized so that each row corresponds to  
#the data for one trading day, into lists containing data 
#that correspond to the extracted column names.
data = [[d[r] for d in data] for r in range(len(col_names))]

#Use the column names as keys and the data lists as values to create a Dictionary. 
data_dict = dict(zip(col_names, data))
#%% 3.
openings = data_dict['Open']
#This list contains NoneType values that must be dealt with before we can do anything else to it.
#The "remove" function doesn't seem to play well with None as an input, so these values
#are converted into the average value of the other elements instead.
openings = remove_nan_values(openings)

#Identify and print the highest and lowest values in the list.
max_opening = max(openings)
min_opening = min(openings)
print(max_opening, min_opening)
     
#%% 4.
highs = data_dict['High']
lows = data_dict['Low']
#Take the difference of each pair of values across the lists.
differences = subtract_value_pairs(highs, lows)

#Round to the hundredths place to keep the value consistent with the supplied data,
# and print the value.
max_dif = round(max(differences), 2)
print(max_dif)

#%% 5.
closings = data_dict['Close']
#Take the difference of each pair of values across the lists.
differences = subtract_value_pairs(openings, closings)

#Round to the hundredths place and print the value.
max_closing_dif = round(max(differences), 2)
print(max_closing_dif)

#%% 6.
volumes = data_dict['Traded Volume']
#Compute and print the average of the values in the list.
avg = compute_average(volumes)
print(avg)

#%% 7.
#Compute and print the median.
med = compute_median(volumes)
print(med)