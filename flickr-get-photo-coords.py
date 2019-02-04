import flickr_api
import psycopg2
import sys
import os

#key_registration
flickr_api.set_keys(api_key = '6b10a1af9fac3ec5230784818b14c922', api_secret = '31568c07bb425ae4')

#parameters
photoList=[]
photos = flickr_api.Photo.search(bbox = '-3.6244, 40.0144, -3.5372, 40.0540', min_taken_date=1415463675, media='photos', extras='description,date_upload,date_taken,geo')
number_of_pages=photos.info.pages
#iterate until counter gets the number of pages
counter=1
while (counter <= number_of_pages):
    photos1 = flickr_api.Photo.search(bbox = '-3.6244, 40.0144, -3.5372, 40.0540', page = counter, min_taken_date=1415463675, media='photos',extras='description,date_upload,date_taken,geo')
    photoList.extend(photos1)
    print 'Doing page %s with %s photos, total: %s in %s pages' % (counter, len(photos1), photos1.info.total, photos1.info.pages)
    counter=counter+1
#connection to the database
try:
    conn=psycopg2.connect("dbname='TPF' user='TPF' host='localhost' password='TPF'")
    print "connection done successfully"    
except:
    print "I am unable to connect to the database"
cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE TPF 
(
 id serial NOT NULL,
 longitude float,
 latitude float,
 geom GEOMETRY (point, 4326),
 CONSTRAINT id_pkey PRIMARY KEY (id)
 );''')
    print "Table created successfully"
except:
    print "table has not been created"
insert = "insert into Flickr (longitude, latitude) values (%s, %s);"


for p in photoList:
    data = (p['longitude'], p['latitude'])
    cursor.execute('''UPDATE Flickr  SET
    geom= st_setsrid(st_MakePoint(longitude, latitude),4326)
    ''')
    cursor.execute(insert, data)

conn.commit()
cursor.close()
conn.close()
print "process completed"
