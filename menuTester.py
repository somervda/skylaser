from menu import Display,MenuItem
import time

display= Display()

menuItems = []
menuItems.append(MenuItem("Planets", "The Planets", 0, 0, 0, 0))
menuItems.append(MenuItem("Satellites", "The ISS, Moon etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Constellations", "The big dipper, orion etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Stars", "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
menuItems.append(MenuItem("Setup", "", 0, 0, 0, 0))


print(len(menuItems))
display= Display()
display.menuItems = menuItems
s=display.showMenu()
display.showSelection(s)
time.sleep(1.5)
display.showText("Thats all folks!")
time.sleep(1.5)


  