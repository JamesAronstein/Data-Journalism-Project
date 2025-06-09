#should have 3 routes

#one for about

#one for index, which has macro

#and one for the micro, where I can use variables to pass in which micro
    #its just one boro.html pg, that generates something different based on which boro is called with render template
    #use if statement, based on which boro, to load which specific svg


#for nav bar, I should have nav bar.html, and dynamically insert it into each one, so if I make changes in the nav bar, I only change it once

#templates folder would have files for: about.html, index.html, micro.html, graph.svg, map.svg (would prob have one for all 5 boros)

#FIGURE OUT WHY THE MAP ISN'T CHANGING COLOR, I TRIED TO GET THE GET SATURATION WORKING



from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__, static_url_path='', static_folder='static')

boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

def get_max_min_pop_neighborhood (borough):
    f = open("data/neighborhood_data.json", "r")
    n_data = json.load(f)
    f.close()

    pop_values = []
    percent_values = []

    for n in n_data[borough]:
        #print (n_data[borough][n])
        pop_values.append(n_data[borough][n][0])
        pop_values.append(n_data[borough][n][1])
        percent_values.append(n_data[borough][n][3])

    min_max = []
    #first element [0] is the min pop, second element [1] is the max pop, #third element [2] is the min %change, fourth element [3] is the max %change

    

    min_max.append(min(pop_values))
    min_max.append(max(pop_values))

    min_max.append(min(percent_values))
    min_max.append(max(percent_values))

    return (min_max)

def get_neighborhood_count (borough):

    f = open("data/neighborhood_data.json", "r")
    n_data = json.load(f)
    f.close()

    n_count = 0

    for n in n_data[borough]:
       n_count+=1

    return n_count

def get_max_min_borough(data):
    #returns a list, [0] is min, [1] is max
    b_pops = []
    for n in data:
        b_pops.append(data[n][3])
    b_pops.sort()

    return (b_pops[0], b_pops[-1])


def get_lightness(data, borough):
    min = get_max_min_borough(data)[0]
    max = get_max_min_borough(data)[1]

    range = max - min
    scale_factor = 80/range

    pop_value =  data[borough][3]


    #the scale here is that this lightness variable is lower for lower pop changes, but I change that in the map.svg, so it's darker for a greater pop change
    lightness = (pop_value - min) * scale_factor

    return {
        "min": min,
        "max": max,
        "range": range,
        "scale_factor": scale_factor,
        "lightness": lightness
        }


@app.route('/')
def index():
    f = open("data/borough_agg_data.json", "r")
    b_agg_data = json.load(f)
    f.close()

   
    
    return render_template('index.html', boroughs = boroughs, b_agg_data = b_agg_data, get_max_min_borough = get_max_min_borough, get_lightness = get_lightness)




@app.route('/micro')
def micro():

    max_pc_borough = {
        "Bronx": 30,
        "Brooklyn": 20,
        "Manhattan": 100,
        "Queens": 20,
        "Staten Island": 30
    }

    bar_height_borough = {
        "Bronx": 17,
        "Brooklyn": 12,
        "Manhattan": 24,
        "Queens": 10,
        "Staten Island": 40
    }

    borough_summary = {}

    for b in boroughs:
        borough_summary[b] = {}
        borough_summary[b]["Neighborhood Count"] = get_neighborhood_count(b)
        borough_summary[b]["Min Pop"] = get_max_min_pop_neighborhood(b)[0]
        borough_summary[b]["Max Pop"] = get_max_min_pop_neighborhood(b)[1]
        borough_summary[b]["Min Percent Change"] = get_max_min_pop_neighborhood(b)[2]
        borough_summary[b]["Max Percent Change"] = get_max_min_pop_neighborhood(b)[3]

    

    

    f = open("data/neighborhood_data.json", "r")
    n_data = json.load(f)
    f.close()

    def get_pc(tup):
        return (tup[1])



    def get_n_pc_order (borough):
        n_pc_pairs = []
        for n in n_data[borough]:
            pc = n_data[borough][n][3]
            #adds a tuple (neighborhood, percent change) to the list that can then be sorted
            n_pc_pairs.append( (n, pc))

        n_pc_sorted = sorted(n_pc_pairs, key = get_pc, reverse = True)

        '''
        n_sorted =  []
        for t in npc_sorted:
            n_sorted.append(t[0])
        '''
       

        return n_pc_sorted

    borough = request.args.get("borough")

    
    return render_template('micro.html', n_data = n_data, boroughs = boroughs, borough = borough, borough_summary = borough_summary, max_pc_borough = max_pc_borough, bar_height_borough = bar_height_borough, get_n_pc_order = get_n_pc_order )

@app.route('/about')
def about():
    return render_template('about.html')



app.run(debug=True)

