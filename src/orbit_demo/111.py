class FirstClass:
    def setdata(self, value):
         self.data = value
    def display(self):
        print(self.data)
        
x = FirstClass()
x.setdata(2)
x.display()