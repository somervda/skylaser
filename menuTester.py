from menu import Display,MenuItem
import time

display= Display()

menuItems = []
menuItems.append(MenuItem("Planets",0, "The Planets", 0, 0, 0, 0))
menuItems.append(MenuItem("Satellites",0, "The ISS, Moon etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Constellations",0, "The big dipper, orion etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Stars",0, "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Setup",0, "", 0, 0, 0, 0))


print(len(menuItems))
display= Display()
display.menuItems = menuItems
s=display.showMenu()
display.showSelection(s)
time.sleep(1.5)
display.showText("Thats all folks!")
time.sleep(1.5)


  