import logging


logger = logging.getLogger('squad.ci.backend')


description = "None"


class Backend(object):

    """
    This is the interface that all backends must implement. Depending on the
    actual backend, it's not mandatory to implement every method.
    """

    def __init__(self, data):
        self.data = data

    def submit(self, test_job):
        """
        Submits a given test job to the backend service.

        The return value must be the job id as provided by the backend.

        On errors, implementations can raise two classes of exceptions:
            * squad.ci.exceptions.SubmissionIssue, when there is an unrecoverable
              issue with the job (such as invalid data).
            * squad.ci.exceptions.TemporarySubmission, when there is a temporary
              condition that stopped the submission from happening that could
              be gone in the future (e.g. a server-side issue or a maintainance
              window).
        """
        pass

    def resubmit(self, test_job):
        """
        Re-submits given test job to the backend service

        The return value must be the re-submitted job id as provided by the
        backend.

        On errors, implementations can raise two classes of exceptions:
            * squad.ci.exceptions.SubmissionIssue, when there is an unrecoverable
              issue with the job (such as invalid data).
            * squad.ci.exceptions.TemporarySubmission, when there is a temporary
              condition that stopped the submission from happening that could
              be gone in the future (e.g. a server-side issue or a maintainance
              window).
        """

    def fetch(self, test_job):
        """
        Fetches data from a given test job from the backend service. It can be
        assumed that the job has been properly submited before, i.e. it has a
        proper id.

        The return value must be a tuple (status, metadata, tests, metrics),
        where status is a string, all other elements are dictionaries.
        """
        pass

    def listen(self):
        """
        Listens the backend service for realtime test results. What to do with
        the received data is up to each specific backend implementation.
        """
        pass

    def job_url(selt, test_job):
        """
        Returns the URL of the test job in the backend
        """
        pass

    def format_message(self, msg):
        return self.data.name + ': ' + msg

    def log_info(self, msg):
        logger.info(self.format_message(msg))

    def log_debug(self, msg):
        logger.debug(self.format_message(msg))

    def log_warn(self, msg):
        logger.warn(self.format_message(msg))

    def log_error(self, msg):
        logger.error(self.format_message(msg))
