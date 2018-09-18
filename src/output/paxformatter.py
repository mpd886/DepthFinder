

class PaxFormatter:

    def write(self, artifacts):
        for a in artifacts:
            print('url("link:classpath:{}.link"),'.format(a.artifact))
