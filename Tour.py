import urllib.request
import re


class Tour(object):
    # A constructor when an object is created that takes zero or more strings as arguments each giving a city name
    # and state abbreviation
    def __init__(self, *city):
        self.__city = []
        for i in city:
            if type(i) == str:
                self.__city.append(i)

    def distance(self, method='driving'):
        self.__distance = 0

        # The general form of a distance query looks like this.
        # http://maps.googleapis.com/maps/api/distancematrix/json?parameters
        # The parameters used here are origin,destination,sensor and mode
        # Example of a query url
        # http://maps.googleapis.com/maps/api/distancematrix/json?origins=New+York+NY&destinations=Lansing+MI&mode=driving&sensor=false

        for i in range(len(self.__city) - 1):
            query_url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=" + re.sub(r'[\W]*\s', '+',self.__city[i])\
                        + "&destinations=" + re.sub(r'[\W]*\s', '+', self.__city[i + 1]) + "&mode=" + method + "&sensor=false"
            web_obj = urllib.request.urlopen(query_url)
            result_str = str(web_obj.read())
            self.__distance += parser(result_str)
        return self.__distance

    # Return the cities to be visited in the tour as a string formatted same as the arguments provided to the constructor
    def __str__(self):
        return ' ----> '.join([c for c in self.__city])

    # string representation of an object
    def __repr__(self):
        return self.__str__()

    # Concatenation of the tour
    def __add__(self, other):
        return Tour(*(self.__city + other.__city))

    # Multiplication method used for repeated concatenation of this tour
    # The argument indicates the number of times to cycle through the cities
    # Hence the argument must be a positive integer,else raises an exception
    def __mul__(self, other):
        if type(other) != int:
            raise TypeError('This is not an integer')
        elif other < 0:
            raise ValueError('Enter a positive integer')
        elif other == 0:
            return Tour()
        else:
            new_tour = []
            for i in range(other):
                new_tour += self.__city
            return Tour(*new_tour)

    # Representation of the multiplication method
    def __rmul__(self, other):
        return self.__mul__(other)

    # Method that compares the driving the driving distance of this tour with other tour
    # Returns TRUE if driving distance of this tour is greater than that of the other tour,else returns FALSE
    def __gt__(self, other):
        return self.__distance > other.__distance

    # Method that compares the driving the driving distance of this tour with other tour
    # Returns TRUE if driving distance of this tour is lesser than that of the other tour,else returns FALSE
    def __lt__(self, other):
        return self.__distance < other.__distance

    # Method that compares this tour with the other tour for equality
    # Tours are compared as equal if they precisely visit the same cities in the same order
    def __eq__(self, other):
        return self.__city == other.__city


def parser(given):
    m = re.search(r'(?<="value" : )[\d]+', given)
    return float(m.group(0))

# The Main Function


def main():
    t1 = Tour("Texas, TX", "Lansing, MI", "Sacramento, CA")
    t2 = Tour("Oakland, CA")
    t3 = Tour("Sacramento, CA", "Oakland, CA")

    print("t1: {}\nt2:{}\nt3:{}".format(t1, t2, t3))
    print("\n")

    # Prints the distances through each mode for a particular tour
    print("t1 distances: driving-{} km; biking-{} km; walking-{} km".format(round(t1.distance() / 1000),round(t1.distance('bicycling') / 1000),
    round(t1.distance('walking') / 1000)))
    print("\n")

    print("Using driving distances from here on.....")
    # Concatenation of tours
    t4 = t1 + t2
    print("t4 is the combination of t1 and t2,details shown below")
    print("t4:", t4)
    print("t4 driving distance:", round(t4.distance() / 1000), "km")
    print("\n")

    # Checking for equality of tours
    print("Equality of Tours")
    print("t4 == t1 + t2:", t4 == t1 + t2)
    if(t4 == t1 + t2):
        print("t4 is a combination of t1 and t2")
    print("\n")

    # Checking for lesser than
    print("Least distance Tour")
    # Checking for lesser than
    print("t1<t2:",t1.distance()<t2.distance())
    if(t1.distance()<t2.distance()):
        print("The distance of tour 1 is lesser")
    else:
        print("The distance of tour 2 is lesser")
    print("\n")

    # Checking for greater than
    print("Tour with greater distance")
    print("t1>t2:",t1.distance()>t2.distance())
    if (t1.distance() > t2.distance()):
        print("The distance of tour 1 is greater")
    else:
        print("The distance of tour 2 is greater")
    print("\n")

    # Repetitive Tours
    print('Repeated Tours')
    print('Cycling through the cities in t3 2 times')
    print('t3*2:',t3*2)
    t5=t3*2
    print('Distance of the Total tour:{}km'.format(round(t5.distance()/1000)))


if __name__ == "__main__":
    main()


# This is how the result_str looks like.This needs to be parsed to get the desired information.
# result_str=b'{\n "destination_addresses" : [ "Lansing, MI, USA" ],\n "origin_addresses" : [ "Texas, USA" ],\n   "rows" : [\n{\n"elements" : [\n{\n"distance" : {\n "text" : "2,117 km",\n"value" : 2116799\n},\n"duration" : {\n"text" : "19 hours 8 mins",\n"value" : 68899\n},\n"status" : "OK"\n}\n]\n }\n],\n "status" : "OK"\n}\n'
