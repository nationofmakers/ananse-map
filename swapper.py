import csv

READFROM = 'spaces.csv'
WRITETO = 'new_spaces.csv'

with open(READFROM, 'rU') as csvfile:
	reader = csv.reader(csvfile)
	with open(WRITETO, 'wb') as fileToWrite:
		writer = csv.writer(fileToWrite)
		
		first = next(reader)
		lat_idx = first.index("Lat")
		lon_idx = first.index("Long")
		writer.writerow(first)

		wrong = ["Impact Hub Madrid"]

		box1 = [[-71.6573, -35.431], [-34.86, -8.02]] #bottom left, top right
		box2 = [[-8.74216, 40.2023788], [24.901795, 60.391263]] #bottom left, top right
		box3 = [[-14.712748, 0], [4.7, 6.9]]
		box4 = [[17.082481, -34.0547105], [31.0280179, -22.5589039]]
		box5 = [[-84.306446, -12], [-40, 50]]
		box6 = [[72.01, 9.01], [90.01, 55.01]]
		box7 = [[-90, -180], [-74, 180]]
		box8 = [[-22.07443, 63.44042419], [-19.6394444, 65.7461111]]
		box9 = [[66.0730106, -23.1328401], [66.0730106, -23.1328401]]

		boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9]

		for row in reader:
			new_row = row
			try:
				lat = float(row[lat_idx])
				lon = float(row[lon_idx])
				flip = False
				for box in boxes:
					low_lat = box[0][0]
					hi_lat = box[1][0]
					low_lon = box[0][1]
					hi_lon = box[1][1]


					top_right = box[1]
					if lat >= low_lat and lat <= hi_lat and lon >= low_lon and lon <= hi_lon:
						flip = True
				if flip:
					new_row[lon_idx] = lat
					new_row[lat_idx] = lon
			except ValueError:
				a = 0
			writer.writerow(new_row)



