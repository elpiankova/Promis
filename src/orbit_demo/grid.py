from PIL import Image, ImageDraw

image = Image.new("RGBA", (320,320), (0,0,0,0)) #новый рисунок с прозрачным фоном
draw = ImageDraw.Draw(image) #создаем обьект ImageDraw и передаем ему рисунок
draw.ellipse((10,10,200,300), outline="red")#рисуем красный эллипс
del draw
image.save("/home/yakim/workspace/Orbit_demo/test.png", "PNG")