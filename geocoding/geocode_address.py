import json
import csv
import urllib2
import urllib

READFROM = 'spaces_new_latlng.csv'
WRITETO = 'spaces_new_latlng_new_address.csv'
headers = ["Source", "ownership", "Region", "Name", "Country", "address", "City and Region", "State", "description", "Simple Category", "Full Category", "E-mail", "Website", "Phone", "Facebook", "Lat", "Long", "Tools", "Short blurb (NULL)", "Fablabs url (NULL)", "wiki_hackerspaces", "Status", "Flickr", "YouTube", "Ustream", "Mailinglist", "Last Updated", "Open to Exchanges?", "IRC", "Date of founding", "Number of members", "Wiki", "Twitter", "GooglePlus / Facebook", "Membership fee", "Jabber", "Open to Residencies?", "City", "State or District", "meetup, Eventbrite", "Size of rooms", "Original Long lat or degrees", "", "g_Address", "g_LatLng", "g_Icon", "g_Id", "g_Place_Id", "g_Name", "", "g_Rating", "g_Types", "open_CONTACT FIRST NAME", "open_CONTACT SURNAME", "open_CONTACT POSITION", "IMAGE URL", "FUNCTION", "THEME", "FORM", "FOCUS", "SUBMITTER FIRST NAME", "SUBMITTER SURNAME", "SUBMITTER EMAIL", "SUBMITTER ORGANISATION", "ADDRESS 1", "ADDRESS 2", "ADDRESS 3", "Address 4", "POSTCODE", "address_open", "description_open", "Full Category_open", "Lat_open", "Long_open", "faire_category", "faire_annual", "faire_name", "faire_year", "faire_event_type", "faire_event_start_date", "", "giz_impact"]
index_dict = {"g_Address" : headers.index("g_Address"), 
				"g_LatLng": headers.index("g_LatLng"), 
				"g_Icon": headers.index("g_Icon"), 
				"g_Id": headers.index("g_Id"), 
				"g_Place_Id": headers.index("g_Place_Id"), 
				"g_Name": headers.index("g_Name"), 
				"g_Rating": headers.index("g_Rating"), 
				"g_Types": headers.index("g_Types")}

num_cols = len(headers)

with open(READFROM, "rU") as csvfile:
	reader = csv.reader(csvfile)
	with open(WRITETO, 'wb') as fileToWrite:
		writer = csv.writer(fileToWrite)
		add_count = 0
		counter = 0
		
		for row in reader:
			if counter==0:
				writer.writerow(headers)
			else:
				if row[headers.index("Lat")] == None or row[headers.index("Long")] == None or row[headers.index("Lat")].strip() == "" or row[headers.index("Long")].strip() == "" or row[headers.index("address")] == None or row[headers.index("address")].strip() == "":


					place = urllib.urlencode({'query':str(row[3])+", "+str(row[6])+", "+str(row[2])})
					key = "AIzaSyBL2oa0rys11SiBts3TnJ9SBAZDKfPvg8s"
					url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"+place+"&key="+key
					data = json.loads(urllib2.urlopen(url).read())
					
					address = row[headers.index("address")]
					latlng = ""
					icon = ""
					gid = ""
					pid = ""
					name = ""
					hours = ""
					rating = ""
					types = ""
					lat = row[headers.index("Lat")]
					lon = row[headers.index("Long")]
					if data['status']=="OK":
						add_count += 1
						print add_count
						if 'results' in data:
							result = data['results']
							if result[0]:
								result = result[0]

								if 'formatted_address' in result:
									address = result['formatted_address']
								if 'geometry' in result:
									loc = result['geometry']['location']
									lat = str(loc['lat'])
									lon = str(loc['lng'])
									latlng = lat+", "+lon
								if 'icon' in result:
									icon = result['icon']
								if 'id' in result:
									gid = result['id']
								if 'place_id' in result:
									pid = result['place_id']
								if 'name' in result:
									name = result['name']
								if 'hours' in result:
									hours = str(result['opening_hours']['weekday_text'])
								if 'rating' in result:
									rating = str(result['rating'])
								if 'types' in result:
									types = str(result['types'])
					row_objects = {"g_Address" : address, 
									"Lat": lat,
									"Long": lon,
									"g_LatLng": latlng, 
									"g_Icon": icon, 
									"g_Id": gid, 
									"g_Place_Id": pid,
									"g_Name": name,
									"g_Rating": rating,
									"g_Types": types}
					for key in row_objects.keys():
						try:
							row[headers.index(key)] = row_objects[key].encode('utf-8').strip()
						except UnicodeDecodeError: 
  							print "ERROR: " + key
				writer.writerow(row)
			counter += 1
