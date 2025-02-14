from menu import Menu,MenuItem

menuItems = []
menuItems.append(MenuItem("Planets", "The Planets", 0, 0, 0, 0))
menuItems.append(MenuItem("Satellites", "The ISS, Moon etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Constellations", "The big dipper, orion etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Stars", "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
menuItems.append(MenuItem("x1", "The Planets", 0, 0, 0, 0))
menuItems.append(MenuItem("x2", "The ISS, Moon etc", 0, 0, 0, 0))
menuItems.append(MenuItem("y1", "The big dipper, orion etc", 0, 0, 0, 0))
menuItems.append(MenuItem("y2", "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
menuItems.append(MenuItem("z1", "The Planets", 0, 0, 0, 0))
menuItems.append(MenuItem("z2222", "The ISS, Moon etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Eagles", "The big dipper, orion etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Giants", "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))

print(len(menuItems))
topMenu= Menu(itemList=menuItems)
s=topMenu.showMenu()
topMenu.displaySelectionOnI2c(s)
  