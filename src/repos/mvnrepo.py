import time
import logging
from bs4 import BeautifulSoup
import requests
from artifacts import Artifact


class InvalidArtifactException(Exception):
    def __init__(self, content):
        """
        :param content: HTML content that caused the exception
        """
        self.content = content

    def __str__(self):
        return "Could not parse HTML '{}'".format(self.content)


def create_href(group, artifact, version):
    return "/".join(["artifact", group, artifact, version])


class MvnParser:
    BASE_URL = 'https://mvnrepository.com'

    def __init__(self):
        self.logger = logging.getLogger('MvnParser')
        self.artifacts = set()

    def get_artifact(self, table_row):
        """Returns an Artifact extracted from the given table row

        The artifacts is in the 4th column.

        href format: /artifact/<group id>/<artifacts id>/<version>
        """
        try:
            cells = table_row.find_all('td')
            href = self._get_href(cells)
            parts = href.split('/')
            artifact = Artifact(parts[2], parts[3], parts[4], href)
            self.logger.debug("Extracted {}".format(artifact))
            return artifact
        except TypeError:
            raise InvalidArtifactException(table_row)

    def _get_href(self, cells):
        """First looks in cells[3] for an anchor tag, if presetn return href attrib
        if cells[3].a is None (sometimes) try, cells[4]

        :raise TypeError: if no anchor tag is present in row
        """
        if cells[3].a is not None:
            return cells[3].a['href']
        else:
            return cells[4].a['href']

    def _get_dependency_divs(self):
        """returns a list of divs that contain dependency information
        """
        divs = self.soup.find_all('div', class_='version-section')
        results = []
        for d in divs:
            if d.h2 is not None:
                if d.h2.text.find("Dependencies") != -1:
                    results.append(d)
        return results

    def _get_artifacts_from_div(self, div):
        self.logger.debug("Getting artifacts for {}".format(div.h2))
        tbody = div.table.tbody
        deps = set()
        for row in tbody.find_all('tr'):
            try:
                deps.add(self.get_artifact(row))
            except InvalidArtifactException as e:
                self.logger.warning("Could not extract artifact: {}", e)
        return deps

    def _parse_dependencies(self):
        """returns a set of artifacts"""
        deps = set()
        for div in self._get_dependency_divs():
            deps = deps.union(self._get_artifacts_from_div(div))
        return deps

    def get_dependency_list(self, artifact):
        self._get_dependencies(artifact)
        return self.artifacts

    def _get_dependencies(self, artifact):
        url = "{}/{}".format(MvnParser.BASE_URL, artifact.href)
        resp = requests.get(url)
        if resp.status_code != 200:
            self.logger.error("Could not retrieve dependencies for artifact {}".format(artifact))
            return

        self.artifacts.add(artifact)
        self.soup = BeautifulSoup(resp.text, 'html.parser')
        for dep in self._parse_dependencies():
            if dep not in self.artifacts:
                time.sleep(1)
                self._get_dependencies(dep)
            else:
                self.logger.debug("Already processed {}".format(dep))
