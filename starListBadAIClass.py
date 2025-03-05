from skyfield.api import load
from skyfield.data import hipparcos

class BrightestStars:
    def __init__(self, top_n=10):
        """
        Initializes the BrightestStars class.
        :param top_n: Number of top brightest stars to retrieve.
        """
        self.top_n = top_n
        self.hipparcos = load.open(hipparcos.URL)
        self.stars = self.hipparcos.entries

    def get_top_stars(self):
        """
        Retrieves the top N brightest stars sorted by visual magnitude.
        :return: List of tuples containing star name (HIP number) and magnitude.
        """
        sorted_stars = sorted(self.stars.items(), key=lambda item: item[1].magnitude)
        top_stars = [(f'HIP {hip}', star.magnitude) for hip, star in sorted_stars[:self.top_n]]
        return top_stars

if __name__ == "__main__":
    bright_stars = BrightestStars(top_n=10)
    for star in bright_stars.get_top_stars():
        print(star)

