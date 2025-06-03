#should have 3 routes

#one for about

#one for index, which has macro

#and one for the micro, where I can use variables to pass in which micro
    #its just one boro.html pg, that generates something different based on which boro is called with render template
    #use if statement, based on which boro, to load which specific svg


#for nav bar, I should have nav bar.html, and dynamically insert it into each one, so if I make changes in the nav bar, I only change it once

#templates folder would have files for: about.html, index.html, micro.html, graph.svg, map.svg (would prob have one for all 5 boros)

#find the life expectancy code on the Trinity shared github

##FIX THE FORMAT DATA TO GET THE VALUES IN NEIGHBORHOOD DATA TO BE NUMS, NOT STRINGS


from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__, static_url_path='', static_folder='static')

boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

def get_max_min_pop (borough):
    f = open("data/neighborhood_data.json", "r")
    n_data = json.load(f)
    f.close()

    pop_values = []

    for n in n_data[borough]:
        print (n_data[borough][n])
        pop_values.append(n_data[borough][n][0])
        pop_values.append(n_data[borough][n][1])

    min_max = []
    #first element [0] is the min, second element [1] is the max

    min_max.append(min(pop_values))
    min_max.append(max(pop_values))

    return (min_max)

def get_neighborhood_count (borough):

    f = open("data/neighborhood_data.json", "r")
    n_data = json.load(f)
    f.close()

    n_count = 0

    for n in n_data[borough]:
       n_count+=1

    return n_count


borough_summary = {}

for b in boroughs:
    borough_summary[b] = {}
    borough_summary[b]["Neighborhood Count"] = get_neighborhood_count(b)
    borough_summary[b]["Min Pop"] = get_max_min_pop(b)[0]
    borough_summary[b]["Max Pop"] = get_max_min_pop(b)[1]

print (borough_summary)





@app.route('/')
def index():
    f = open("data/borough_agg_data.json", "r")
    #data = json.load(f)
    f.close()
    
    return render_template('index.html', boroughs = boroughs)




@app.route('/micro')
def micro():
    f = open("data/neighborhood_data.json", "r")
    #data = json.load(f)
    f.close()

    borough = request.args.get("borough")
    
    return render_template('micro.html', boroughs = boroughs, borough = borough)

@app.route('/about')
def about():
    return render_template('about.html')



app.run(debug=True)

