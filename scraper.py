import urllib2
import json
from pymongo import MongoClient

def main():
	for i in xrange(649,1155):
		page = getImgurPage(i)
		if not page:
			continue
		print "**** Started inserting Page #",i
		storeImgurHit(page, i)
		print "**** Finished inserting Page #",i
		log("Scraped page #"+str(i)+"\n")
		
def storeImgurHit(page, num):
	if page and page['success'] is True:
		for p in page['data']:
			try:
				hitResp = urllib2.urlopen('http://imgur.com/gallery/'+ p['hash'] + '/comment/best/hit.json')
				hitData = json.load(hitResp) 
				hits.insert(hitData)
				print "Inserted hit #",hits.count()
			except:
				"@@@@@@@@@ Error: Failed to insert a hit"
				log("Error: Failed to insert a hit from page #"+str(num)+"\n")
				continue

def getImgurPage(page):	# 1154 = max = Jan 2, 2011
	try:
		daysAgo = str(page)	# 1 = today, 2 = yesterday...
		galleryResp = urllib2.urlopen('http://imgur.com/gallery/hot/viral/page/' + daysAgo + '/hit.json')
		return json.load(galleryResp)  
	except:
		print "@@@@@@@@@ Error: Failed to load Page #", page
		log("Error: Failed to load Page #"+str(page)+"\n")
		return False

def log(message):
	with open("log.txt", "a") as myfile:
		myfile.write(message)

client = MongoClient()
db = client.imgur
hits = db.hits
main()