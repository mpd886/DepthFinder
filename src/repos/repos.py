from .mvnrepo import MvnParser


MVNREPOSITORY = "mvnrepository"


class UnknownRepositoryException(Exception):
    def __init__(self, repo_name):
        self.repo = repo_name

    def __str__(self):
        return "Unknown repository: {}".format(self.repo_name)


def get_package_repo_handler(repo_name):
    """
    Returns a handler object that can communicate with the specified repository
    :param repo_name:
    :return:
    """
    repos = {MVNREPOSITORY: MvnParser()}
    if repo_name not in repos:
        raise UnknownRepositoryException(repo_name)
    return repos[repo_name]
