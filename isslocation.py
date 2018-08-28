#!/usr/bin/env python

"""ISS Location Finder
Program obtains a list of the astronauts who are currently in space.
It prints their full names, the spacecraft they are currently on board,
and the total number of astronauts in space
Prints current geographic coordinates (lat/lon) of
the space station, along with a timestamp.
In addition, it creates a graphics screen with the world map background image
that displays the ISS's location.
"""

import requests
import turtle
import time


def get_astronauts_list(req_url):
    r = requests.get(req_url)
    data = r.json()
    for item in data:
        if item == 'number':
            print "Total number of astronauts in space: " + str(data[item])
        elif item == 'people':
            for sub_item in data[item]:
                print "Name: " + \
                    sub_item.get('name') + ", Sapcecraft: " + \
                    sub_item.get('craft')


def find_geo_coords(req_url):
    r = requests.get(req_url)
    data = r.json()
    lat_lon = None
    for k, v in data.items():
        if k == 'timestamp':
            print "Timestamp: " + str(data[k])
        elif k == 'iss_position':
            lat_lon = v
            print "Longitude: " + \
                v.get('longitude') + " Latitude: " + v.get('latitude')
    return lat_lon


def find_pass_time(req_url, lat_lon):
    latitude = lat_lon.get('latitude')
    longitude = lat_lon.get('longitude')
    url = req_url + "?lat="+latitude+"&lon="+longitude
    r = requests.get(url)
    data = r.json()
    print ("Next time the ISS will be overhead of Indianapolis IN: " +
           time.ctime(data['response'][0]['risetime']))


def create_iss_map(lat_lon):
    latitude = float(lat_lon.get('latitude'))
    longitude = float(lat_lon.get('longitude'))
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('map.gif')
    iss = turtle.Turtle()
    screen.register_shape("rocket.gif")
    iss.shape("rocket.gif")
    iss.setheading(90)
    iss.penup()
    iss.goto(longitude, latitude)
    screen.title("ISS Location")
    turtle.done()
    screen.exitonclick()


def main():
    get_astronauts_list('http://api.open-notify.org/astros.json')
    lat_lon = find_geo_coords('http://api.open-notify.org/iss-now.json')
    indy_lat_lon = {"latitude": "39.768403", "longitude": "-86.158068"}
    find_pass_time('http://api.open-notify.org/iss-pass.json', indy_lat_lon)
    create_iss_map(lat_lon)


if __name__ == '__main__':
    main()
