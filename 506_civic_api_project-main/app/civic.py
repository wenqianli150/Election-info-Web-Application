from urllib import response

import requests
import urllib.parse

def find_elections(address):
    key = "AIzaSyChoPmgba9gssA5FhyJkhpo9URGP1A9x2w"
    address = address.replace(" ", "%20").replace(",","")
    election_url = "https://civicinfo.googleapis.com/civicinfo/v2/voterinfo?address=" + address + "&key=" + key
    try:
        election_response = requests.get(election_url)
        election_response.raise_for_status()
        return election_response.json()
    except requests.exceptions.HTTPError:
    	return None

def find_reps(address):
    key = "AIzaSyChoPmgba9gssA5FhyJkhpo9URGP1A9x2w"
    address = address.replace(" ", "%20").replace(",", "")
    rep_url = "https://www.googleapis.com/civicinfo/v2/representatives?address=" + address + "&key=" + key

    rep_response = requests.get(rep_url).json()
    return rep_response
    
def validateAddress(address):
    api_key = 'AIzaSyDEksQzo5Tx4zRvPYf_xerwKoaXRcOR7hw'
    encodedaddress=urllib.parse.quote_plus(address)
    geocodeapi = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ encodedaddress + '&key=' + api_key
    response = requests.get(url=geocodeapi)
    data = response.json()
    return data
    
def find_directions(response, address):
    origin = address.replace(" ", "%20").replace(",", "%2C")
    url = "https://www.google.com/maps/dir/?api=1&"
    try:
        for polling_location in response["pollingLocations"][0:5]:
            destination = polling_location["address"]["line1"] + "," +  polling_location["address"]["city"]
            destination = destination.replace(" ", "%20").replace(",","%2C")
            polling_location["directions"] = url + "origin=" + origin + "&destination=" + destination
    except TypeError:
    	return None
    try:
        for early_site in response["earlyVoteSites"][0:5]:
            destination = early_site["address"]["line1"] + "," + early_site["address"]["city"]
            destination = destination.replace(" ", "%20").replace(",", "%2C")
            early_site["directions"] = url + "origin=" + origin + "&destination=" + destination
    except KeyError:
        pass
    try:
        for dropoff in response["dropOffLocations"][0:5]:
            destination = dropoff["address"]["line1"] + "," + dropoff["address"]["city"]
            destination = destination.replace(" ", "%20").replace(",", "%2C")
            dropoff["directions"] = url + "origin=" + origin + "&destination=" + destination
    except KeyError:
        pass
    return response
