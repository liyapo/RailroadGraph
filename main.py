# Definition of RailroadGraph class with an empty dictionary self.all_trips

class RailroadGraph:
    
    def __init__(self):
        self.all_trips = {}
        


    # transforming string_graph ("AB5, BC4, ...") into dictionary with all possible routes
    # dictionary looks like {'AB':[5, 1], 'BC':[4, 1], ..., 'ADEB': [14, 3], 'CEBC': [9, 3], ...}
    def build (self, string_graph, count):
        self.all_trips = self.transform_graph_dictionary(count, string_graph, self.all_trips)

        

    # calculating the distances between the cities if railroads between them exsist
    # if a railroad does not exsist then the message "NO SUCH ROUTE" is returned
    # the name of cities(nodes) should be entered with "-" in between, e.g. "A-B-C" 
    def calculate_distance(self, string_nodes):
        key_nodes = ""
        key_nodes = string_nodes.replace("-", "")
        distance = 0
        try:
            distance = self.all_trips[key_nodes][0]
            return distance
        except KeyError:
            return "NO SUCH ROUTE" 



    # calculating number of trips between two cities with number of stops limited to max_num_stops
    # the name of cities(nodes) should be entered with "-" in between, e.g. "A-C" 
    def calculate_trips_max_stops(self, string_nodes, max_num_stops):

        list_nodes = string_nodes.split("-")
        arrival = list_nodes[-1]
        departure = list_nodes[0]
        num_trips_found = 0
        trips_search = {}
        trips_found = {}
        
        # finding all the trips with number of stops <= max_num_stops
        for key in self.all_trips:    
            if self.all_trips[key][1] <= max_num_stops:
                trips_search[key] = self.all_trips[key]
        # in found trips looking for trips with departure and arrival as required
        for key in trips_search:
            if key[0] == departure and key[-1] == arrival:
                trips_found[key] = trips_search[key] 
                num_trips_found += 1 
        return num_trips_found



    # calculating number of trips between two cities with number of stops equal to exact_num_stops
    # the name of cities(nodes) should be entered with "-" in between, e.g. "A-C" 
    def calculate_trips_exact_number_stops(self, string_nodes, exact_num_stops):

        list_nodes = string_nodes.split("-")
        arrival = list_nodes[-1]
        departure = list_nodes[0]
        num_trips_found = 0
        trips_search = {}
        trips_found = {}
        
        # finding all the trips with number of stops = exact_num_stops
        for key in self.all_trips:    
            if self.all_trips[key][1] == exact_num_stops:
                trips_search[key] = self.all_trips[key]
        # in found trips looking for trips with departure and arrival as required
        for key in trips_search:
            if key[0] == departure and key[-1] == arrival:
                trips_found[key] = trips_search[key] 
                num_trips_found += 1 
        
        return num_trips_found



    # calculating shortest route between two cities 
    # the name of cities(nodes) should be entered with "-" in between, e.g. "A-C" 
    def calculate_shortest_route(self, string_nodes):
        list_nodes = string_nodes.split("-")
        arrival = list_nodes[-1]
        departure = list_nodes[0]
        shortest_distance = 0
        trips_search = {}
        trips_found = {}
        
        # finding all the trips with number of stops >= 2, 
        # which means that we don't take into account direct routes
        for key in self.all_trips:    
            if self.all_trips[key][1] >= 2:
                trips_search[key] = self.all_trips[key]
        # in found trips looking for trips with departure and arrival as required
        for key in trips_search:
            if key[0] == departure and key[-1] == arrival:
                trips_found[key] = trips_search[key] 
        # in found trips finding the shortest distance
        shortest_distance = trips_found.popitem()[1][0]
        for key in trips_found:
            if trips_found[key][0] < shortest_distance:
                shortest_distance = trips_found[key][0]      
        return shortest_distance



    # calculating the number of different trips possible from onw town to another
    # with the distance of the route limited to distance_less_than
    def calculate_number_diff_routes(self, string_nodes, distance_less_than):
        number_diff_trips = 0
        list_nodes = string_nodes.split("-")
        arrival = list_nodes[-1]
        departure = list_nodes[0]
        trips_search = {}
        trips_found = {}        

        # finding all the trips with the distance of the route < distance_less_than
        for key in self.all_trips:    
            if self.all_trips[key][0] < distance_less_than:
                trips_search[key] = self.all_trips[key]
        # in found trips looking for trips with departure and arrival as required
        for key in trips_search:
            if key[0] == departure and key[-1] == arrival:
                trips_found[key] = trips_search[key]
                number_diff_trips +=1

        return number_diff_trips
    
#--------------------------------------------------------------------------------------------------------

# Transforming initial graph into a dictionary with all possible trips, the maximum 
# number of maximum stops possible of the railroad is controlled by vaiable 'count', 
# (number of maximum stops possible) = 2^(count)
# 'count' represents the number of times the recursive function is called to fill in the dictionary

#--------------------------------------------------------------------------------------------------------

    def transform_graph_dictionary(self, count, string_graph, trips):
        
        # putting all direct trips from string_graph in dictionary trips
        # with route as a key and list of values [distance, number of stops]

        # replacing ", " with no space and splitting the merged string into 
        # strings(routes, e.g. 'AB') and numbers(distances, e.g. '5')
        # final list looks like ['AB', '5', 'BC', '4', ...]
        
        string = string_graph.split(", ")
        list_keys_distance = []
        for i in range(len(string)):
            list_keys_distance.append(string[i][0] + string[i][1])
            list_keys_distance.append(string[i][2:])
    

        list_keys = []
        list_distance = []
        # for direct routes there is always only one stop
        stops = 1
        # filling list_keys with all direct routes, e.g. ['AB', 'BC', ...]
        list_keys = [list_keys_distance[i] for i in range(len(list_keys_distance)) if i % 2==0]
        # filling list_distances with integer values of distances, e.g. [5, 4, ...]        
        list_distance = [int(list_keys_distance[i]) for i in range(len(list_keys_distance)) if i % 2 == 1]

        # creating initial dictionary with direct routes, given in the graph, 
        # where the key is the rote and the value is the list [distance, stops]
        for i in range(len(list_keys)):
            trips[list_keys[i]] = [list_distance[i], stops]

        # making a dictionary of all possible trips as a key and 
        # values' list [distance, number of stops]

        return self.create_all_trips(count, trips)


    # adding new trips by merging the existing routes
    def fun_iter(self, trips):
        trips_iter = {}
        merged_iter_dict = trips
        stops = 0

        # going through the dictionary to check which routes can be merged
        # creating new routes, adding new routes and their distances to {trips_iter}
        for key1 in trips:
            for key2 in trips:
                if key1[-1] == key2[0]:
                    distance = 0
                    route = key1 + key2[1:]
                    stops = len(route) - 1
                    distance = trips[key1][0] + trips[key2][0]
                    trips_iter[route] = [distance, stops]               

        # merging the initial dictionary with the new trips
        merged_iter_dict.update(trips_iter)
        return merged_iter_dict

    # recursive function to fill in the dictionary with all possible trips, the maximum 
    # number of stops is equal to 2^count, e.g. if count=3, number of stops maximal = 8
    # this function does not save the created dictionary, it is done in create_all_trips
    def recur(self, count, trips):

        if count == 0:
            pass
        else:
            trips_recur = trips
            trips.update(self.fun_iter(trips_recur))
            return self.recur(count - 1, trips)

    # function to save the dictionary created during the recursion
    def create_all_trips(self, count, trips):

        self.all_trips = trips
        self.recur(count, self.all_trips)
        return self.all_trips
        

      





        
        

