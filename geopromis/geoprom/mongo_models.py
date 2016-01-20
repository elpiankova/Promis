from mongoengine import*

connect('geopromis')

class Data(Document):
    magnetic_field = StringField(required=True)
    electric_field = StringField(max_length=50)   