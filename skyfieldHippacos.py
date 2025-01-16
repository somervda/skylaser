from skyfield.api import Star, load
from skyfield.data import hipparcos

print("getting hipparcos.URL:", hipparcos.URL)
with load.open(hipparcos.URL) as f:
    print("loading dataframe")
    df = hipparcos.load_dataframe(f)

barnards_star = Star.from_dataframe(df.loc[87937])

print("loading de421.bsp")
planets = load('de421.bsp')

print("calculating barnards_star position")
earth = planets['earth']

ts = load.timescale()
t = ts.now()
astrometric = earth.at(t).observe(barnards_star)
ra, dec, distance = astrometric.radec()
print(ra)
print(dec)