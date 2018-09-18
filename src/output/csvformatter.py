import sys
import csv


class CsvOutputter:
    def write(self, artifacts):
        """

        :param artifacts: iterable object of Artifacts
        :param filename:  filename to send output
        :return:
        """
        writer = csv.writer(sys.stdout, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for artifact in artifacts:
            writer.writerow([artifact.group, artifact.artifact, artifact.version])