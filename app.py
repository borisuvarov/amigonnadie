"""
A simple CLI to DOHMH New York City Restaurant Inspection Results.

# TODO: Refactor this pile of cra... "prototype"
"""

import itertools

import colorama
import fire
from sodapy import Socrata


class OpenDataRequester:
    """A simple class to encapsulate app's logic."""

    @staticmethod
    def _request_data_from_api(venue):
        with Socrata("data.cityofnewyork.us", None) as client:
            result = client.get(
                'xx67-kt59',
                q=venue,
                exclude_system_fields=True)
        return result

    @staticmethod
    def _process_result(result):
        streets = {el['street'] for el in result}

        if len(streets) > 1:
            street = input(
                '\nToo many venues with this particular name, please specify '
                'the street to narrow the search' + colorama.Fore.GREEN + '>>')
            result = [
                el for el in result if street.lower() in el['street'].lower()]

        sorted_result = sorted(result, key=lambda x: x['building'])
        grouped_data = [
            sorted(building_data,
                   key=lambda x: x['inspection_date'],
                   reverse=True)
            for _, building_data in itertools.groupby(
                sorted_result,
                key=lambda x: x['building'])]
        data_by_venue = []
        for building_data in grouped_data:
            venue_name = building_data[0]['dba']
            venue_address = '{} {}'.format(
                building_data[0]['building'], building_data[0]['street'])
            is_latest_inspection_ok = (
                    'no violations' in building_data[0]['action'].lower())
            violations = []
            for inspection in building_data:
                violations.append(inspection['violation_description'])
            data_by_venue.append(dict(
                venue_name=venue_name,
                venue_address=venue_address,
                is_latest_inspection_ok=is_latest_inspection_ok,
                violations=violations))
        return data_by_venue

    @staticmethod
    def _print_out_result(data_by_venue):
        for venue_dict in data_by_venue:
            print('----------')
            print('Venue name: {}'.format(venue_dict['venue_name']))
            print('Venue address: {}'.format(venue_dict['venue_address']))
            if venue_dict['is_latest_inspection_ok']:
                print('Last inspection was OK')
                # TODO: add former violations
            else:
                print(
                    colorama.Fore.RED + colorama.Style.BRIGHT +
                    'VIOLATIONS found at the time of the last inspection.\n'
                    'Full list of current and former violations:')
                for number, violation in enumerate(venue_dict['violations']):
                    print('{}. {}'.format(number, violation))
                print(colorama.Fore.RED + 'Still wanna go there?..')

    def check(self, venue):
        colorama.init(autoreset=True)

        result = self._request_data_from_api(venue)
        data_by_venue = self._process_result(result)
        self._print_out_result(data_by_venue)

        colorama.deinit()


def main():
    fire.Fire(OpenDataRequester)


if __name__ == '__main__':
    main()
