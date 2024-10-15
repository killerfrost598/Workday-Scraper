import re

def key_extracter(url):
    pattern = r"https?://?([a-zA-Z-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def date_extracter(date):
    pattern = r"\b(\d+)\b\s+Days\s+Ago" 
    if date == "Posted Today":
        return 0
    elif date == "Posted Yesterday":
        return 1
    elif date == "Posted 30+ Days Ago":
        return 31
    else:
        return int(re.search(pattern, date).group(1))

def mean_freq(dictionary):
    newdict = {'Company_name':'','frequency':{}}
    for key in dictionary['frequency']:
        newdict['frequency'][date_extracter(key)] = dictionary['frequency'][key]
        newdict['Company_name'] = dictionary['Company_name']
    return newdict

def isseq(array):
    elements = []
    for i in array:
        elements.append(date_extracter(i))
    return elements

# print(re.findall(r"\d+", "Posted 2+ days ago"))