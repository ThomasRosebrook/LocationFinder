import math

#Class to define a specific place
class Place:
    def __init__(self, place_name="", x_pos=0, y_pos=0, length=1, width=1):
        self.name = place_name
        self.x = x_pos
        self.y = y_pos
        self.length = length
        self.width = width
        self.coordinates = [self.x, self.y]
        self.dimensions = [self.length, self.width]
    
    def print_name(self):
        print(self.name)
    
    def print_self(self):
        print(f"\n{self.name}: \nCoordinates: {self.coordinates} \nDimensions: {self.length} x {self.width}")
        
    
#Method to convert file into a dictionary of place objects
def open_file(file_name="blocks"):

    places = {}
    counter = 0;
    
    with open(file_name, 'r') as file:
    
            for line in file:
            
                line = line.strip()
                counter += 1
                if not line == "":
                
                    line = line.split(",", 4)
                    
                    place_name = ""
                    
                    for letter in line[0].upper():
                        if not letter == " " and not letter == "-":
                            place_name += letter
                    
                    raw_name = line[0]
                    x = int(line[1])
                    y = int(line[2])
                    length = int(line[3])
                    width = int(line[4])
                    
                    places[place_name] = Place(raw_name, x, y, length, width)
                    
                    if (counter == 1):
                        places["Center"] = Place(raw_name, x, y, length, width)
    
    return places

#method to select file based on user input
def get_file():
    print("Where do you want to have directions for? \nEnter [KSU] for K-State, [Blocks] for the example, or a full filename for a custom input file")
    choice = input("Enter campus choice: ").lower()
    
    file_name = ""
    
    if choice == "blocks":
        file_name = "blocks.txt"
    elif choice == "ksu":
        file_name = "ksu.txt"
    else:
        file_name = choice

    
    return file_name
    
#method to calculate the distance between two place objects
def calc_distance(dimensions_one, dimensions_two, coords_one = [0,0], coords_two = [0,0]):
    
    x_one = 0
    x_two = 0
    y_one = 0
    y_two = 0
    
    if coords_two[0] > coords_one[0]:
        x_two = coords_two[0] - (dimensions_two[0] / 2)
        x_one = coords_one[0] + (dimensions_one[0] / 2)
    elif coords_two[0] < coords_one[0]:
        x_two = coords_two[0] + (dimensions_two[0] / 2)
        x_one = coords_one[0] - (dimensions_one[0] / 2)
    
    if coords_two[1] > coords_one[1]:
        x_two = coords_two[1] - (dimensions_two[1] / 2)
        x_one = coords_one[1] + (dimensions_one[1] / 2)
    elif coords_two[1] < coords_one[1]:
        y_two = coords_two[1] + (dimensions_two[1] / 2)
        y_one = coords_one[1] - (dimensions_one[1] / 2)
    
    
    x_diff = x_two - x_one
    y_diff = y_two - y_one
    
    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
    
    return distance

#method to calculate what direction a desired place is from the place the user currently is at
def calc_direction(dimensions_one, dimensions_two, coords_one = [0,0], coords_two = [0,0]):
    
    direction = ["", "", "same"]
    
    x_one = coords_one[0]
    x_two = coords_two[0]
    y_one = coords_one[1]
    y_two = coords_two[1]
    
    
    if x_two > x_one:
        direction[0] = "east"
    elif x_two < x_one:
        direction[0] = "west"
    
    if y_two > y_one:
        direction[1] = "north"
    elif y_two < y_one:
        direction[1] = "south"
    
    if not (x_two + dimensions_two[0] > x_one - dimensions_one[0]) or not (x_two - dimensions_two[0] < x_one + dimensions_one[0]):
        direction[2] = "diff"
    elif not (y_two + dimensions_two[1] > y_one - dimensions_one[1]) or not (y_two - dimensions_two[1] < y_one + dimensions_one[1]):
        direction[2] = "diff"
    
    return direction

#method to get user input for a building
def get_building(places, current_location = True):
    
    building_output = Place("", 0, 0, 0, 0)
    
    building_not_found = True
    
    while building_not_found:
    
        if current_location:
            building_input = input("\nWhat location are you at? ").upper()
        else:
            building_input = input("\nWhat location are you looking for? ").upper()
        
        
        building_name = ""
        
        
        for letter in building_input:
            if not letter == " " and not letter == "-" and not letter == ".":
                building_name += letter
        
        if building_name[-4:] == "HALL":
            building_name = building_name[0:-4]
        
        if building_name in places:
            building_output = places[building_name]
            building_not_found = False
        else:
            print("Error: Building not found \nEither the building name was misspelled or does not exist")
    
    return building_output
    
#primary method that runs
def main():
    
    file_choice = get_file()
    
    places = open_file(file_choice)
    
    continue_search = "Y"
    
    while continue_search == "Y":
        current_building = get_building(places, True)
        desired_building = get_building(places, False)
        
        current_location = current_building.coordinates
        desired_location = desired_building.coordinates
        
        distance = calc_distance(current_building.dimensions, desired_building.dimensions, current_location, desired_location)
        direction = calc_direction(current_building.dimensions, desired_building.dimensions, current_location, desired_location)
        
        print("\nDistance and Directions:")
        if direction[1] == "" and direction[0] == "":
            print("Locations are the same")
        elif direction[1] == "":
            print(f"Approximate distance from {current_building.name} to {desired_building.name}: {round(distance, 2)} feet")
            print(f"Direction: due {direction[0]}")
        elif direction[0] == "":
            print(f"Approximate distance from {current_building.name} to {desired_building.name}: {round(distance, 2)} feet")
            print(f"Direction: due {direction[1]}")
        else:
            print(f"Approximate distance from {current_building.name} to {desired_building.name}: {round(distance, 2)} feet")
            print(f"Direction: {direction[1]} {direction[0]}")
        
        if direction[2] == "same" and not (direction[1] == "" and direction[0] == ""):
            print("(Locations are in the same building)")
        
        central_location = places["Center"]
        dist_to_center = calc_distance(central_location.dimensions, current_building.dimensions, central_location.coordinates, current_location)
        central_direction = calc_direction(central_location.dimensions, current_building.dimensions, central_location.coordinates, current_location)
        
        print(f"\nIn relation to {central_location.name}")
        if central_direction[1] == "" and central_direction[0] == "":
            print(f"{central_location.name} is your current location")
        elif central_direction[1] == "":
            print(f"Approximate distance to {central_location.name}: {round(dist_to_center, 2)} feet")
            print(f"Direction of {central_location}: due {central_direction[0]}")
        elif central_direction[0] == "":
            print(f"Approximate distance to {central_location.name}: {round(dist_to_center, 2)} feet")
            print(f"Direction: due {central_direction[1]}")
        else:
            print(f"Approximate distance to {central_location.name}: {round(dist_to_center, 2)} feet")
            print(f"Direction: {central_direction[1]} {central_direction[0]}")
            
        continue_search = input("\nDo you wish to search again? (Enter 'Y' for yes): ").upper()






main()