import requests
from skyfield.api import load
from skyfield.data import hipparcos

class DownloadManager():
    def checkInternet(self):
        # Use google as url for testing we can cannect to the internet
        url = 'https://www.google.com'  
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("You are connected to the internet.")
                return True
            else:
                print("Connection issue. Received non-200 status code.")
                return False
        except requests.ConnectionError:
            print("No internet connection.")
            return False
        except requests.Timeout:
            print("The request timed out. Check your network.")
            return False

    def downloadHippacos(self):
        print("downloading hipparcos")
        try:
            load.open(hipparcos.URL)
        except Exception as e:
            print("Error downloading hipparcos:",e)
        print("Done")

    def downloadDe421(self):
        print("downloading de421 JPL planet ephemeris")
        try:
            planets=load('de421.bsp')
        except Exception as e:
            print("Error downloading de431:",e)
        print("Done")

    def downloadSatellites(self):
        print("downloading satellite data")

        max_days = 7.0         # download again once 7 days old
        name = 'satellites.csv'  # custom filename, not 'gp.php'

        base = 'https://celestrak.org/NORAD/elements/gp.php'
        url = base + '?GROUP=active&FORMAT=csv'

        if not load.exists(name) or load.days_old(name) >= max_days:
            load.download(url, filename=name)
        print("Done")


if __name__ == "__main__":
    dm=DownloadManager()
    if dm.checkInternet():
        dm.downloadHippacos()
        dm.downloadDe421()
        dm.downloadSatellites()