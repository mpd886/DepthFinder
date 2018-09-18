import sys
import argparse
import logging
from collections import namedtuple
from artifacts import Artifact
import repos
import output


class DepthFinder:
    def __init__(self, args):
        """
        :param args: DepthFinderArgs
        """
        # root search attributes
        self.root_artifact = Artifact(args.group,
                                      args.artifact,
                                      args.version,
                                      repos.create_href(args.group, args.artifact, args.version))
        # keeps track of artifacts we've already searched for
        self.logger = logging.getLogger('DepthFinder')

    def get_dependency_list(self):
        handler = repos.get_package_repo_handler(repos.MVNREPOSITORY)
        return handler.get_dependency_list(self.root_artifact)


def main():
    configure_logging()
    args = parse_args()
    depthfinder = DepthFinder(args)
    artifacts = depthfinder.get_dependency_list()
    writer = output.get_formatter(output.PAX_FORMAT)
    writer.write(artifacts)


def configure_logging():
    logging.basicConfig(level=logging.DEBUG, filename='depthfinder.log')


DepthFinderArgs = namedtuple("DepthFinderArgs", ['group', 'artifact', 'version'])


def parse_args():
    """Returns a DepthFinderArgs tuple of command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--group")
    parser.add_argument("--artifact")
    parser.add_argument('--version')

    args = parser.parse_args()
    if None in [args.group, args.artifact, args.version]:
        parser.print_help()
        sys.exit(1)

    return DepthFinderArgs(args.group, args.artifact, args.version)


if __name__ == "__main__":
    main()
