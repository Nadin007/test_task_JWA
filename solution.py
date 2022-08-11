from dataclasses import dataclass
import json
from typing import Dict, List


@dataclass
class StarStat:
    name: str
    movies_count: int
    rating: float

    def print(self):
        avg_rating = '{:.2f}'.format(self.rating/self.movies_count)
        star_name = f'\'{self.name}\''.ljust(25)
        return f'Star Name: {star_name} | Movies: {self.movies_count} |   AVG Rating: {avg_rating}'


def json_reader(file: str) -> List:
    '''Takes a json file, parses it and returns a list of dictionaries.'''
    with open(file, 'r') as json_file:
        return json.loads(json_file.read())


def group_by_star(list_movies: List) -> Dict[str, StarStat]:
    '''
    Takes a list of dictionaries, groups it by star name.
    Calculates movie statistics for each star.
    '''

    stars_stat = {}
    for movie in list_movies:
        for star in movie['stars'].split(', '):
            if star not in stars_stat:
                stars_stat[star] = StarStat(star, 0, 0)
            star_stat = stars_stat[star]
            star_stat.movies_count += 1
            star_stat.rating += float(movie['rating'])
    return stars_stat


def prepare_data(stars_stat: Dict[str, StarStat]) -> List[StarStat]:
    '''
    Filters stars with amount of movies more than one.
    Sort by the number of movies in an ascending order.
    '''

    filtered_stars_stat = [
        star for star in stars_stat.values() if star.movies_count > 1]
    return sorted(filtered_stars_stat, key=lambda stat: stat.movies_count)


def print_stars(filtered_stars_stat: List[StarStat]) -> None:
    '''Prints data in the required format.'''
    for star in filtered_stars_stat:
        print(star.print())


if __name__ == '__main__':
    list_movies = json_reader('data.json')
    stars_stat = group_by_star(list_movies)
    prepared_data = prepare_data(stars_stat)
    print_stars(prepared_data)
