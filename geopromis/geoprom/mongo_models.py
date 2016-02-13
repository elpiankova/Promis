from mongoengine import*

# Connecting to the database MongoDB
connect('geopromis')

class Data(Document):
	'''
	This is basic class that create ODM for MongoDB instance
	'''
	magnetic_field = StringField(required=True)
	electric_field = StringField(max_length=50)   