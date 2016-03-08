# Email Exercise

1- *What's your proudest achievement? It can be a personal project or something you've worked on professionally. Just a short paragraph is fine, but I'd love to know why you're proud of it.*

After 5 years of development, on the work engine i had been working on, the company went bankrupt. I wanted to release some piece of code badly. With this motivation i started my former job. I inherited a unlayered PHP application, on which i immediately decided to make the codebase service oriented. It took 3 months to re-write the whole system, from scratch. The day of the release was a lot of stress and incredible satisfaction.

2- *Write some code, that will flatten an array of arbitrarily nested arrays of integers into a flat array of integers. e.g. [[1,2,[3]],4] -> [1,2,3,4].*

```
 def flatten(unflattened_list):
    result = []
    for element in unflattened_list:
        if isinstance(element, list):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result
```

3- *We have some customer records in a text file (customers.json) -- one customer per line, JSON-encoded. We want to invite any customer within 100km of our Dublin office (GPS coordinates 53.3381985, -6.2592576) for some food and drinks on us. Write a program that will read the full list of customers and output the names and user ids of matching customers (within 100km), sorted by user id (ascending).*

Can find the source code in GeoSearch.py. It iterates over the input file using a generator function, and checks the distance of the user to the given parameter. It utilizes the Vincenty formula, which is provided in the wiki link shared with the assignment. Although i have implemented 3 seperate algoritms, which you can find in **geo_distance** function.

It uses a heap queue to keep a sorted list of users. This way it doesn't have to sort the users afterwards.

Sample Usage:
> python GeoSearch.py 53.3381985 -6.2592576 100 customers.json

Parameters in order are: **latitude, longitude, distance, input_file**

## Time Schedule
12:21 - Creation of repo

12:34 - Completed first and second questions

13:11 - Break

13:21 - Back from break

13:48 - Finished implementation

13:57 - Finished final formatting