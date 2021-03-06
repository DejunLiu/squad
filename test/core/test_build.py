from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone


from squad.core.models import Group, Build


class BuildTest(TestCase):

    def setUp(self):
        self.group = Group.objects.create(slug='mygroup')
        self.project = self.group.projects.create(slug='myproject')

    def test_version_from_name(self):
        b = Build.objects.create(project=self.project, name='1.0-rc1')
        self.assertEqual('1.0~rc1', b.version)

    def test_name_from_version(self):
        b = Build.objects.create(project=self.project, version='1.0-rc1')
        self.assertEqual('1.0-rc1', b.name)
        self.assertEqual('1.0~rc1', b.version)

    def test_default_ordering(self):
        now = timezone.now()
        before = now - relativedelta(hours=1)
        newer = Build.objects.create(project=self.project, version='1.1', datetime=now)
        Build.objects.create(project=self.project, version='1.0', datetime=before)

        self.assertEqual(newer, Build.objects.last())

    def test_test_summary(self):
        build = Build.objects.create(project=self.project, version='1.1')
        env = self.project.environments.create(slug='env')
        suite = self.project.suites.create(slug='tests')
        test_run = build.test_runs.create(environment=env)
        test_run.tests.create(name='foo', suite=suite, result=True)
        test_run.tests.create(name='bar', suite=suite, result=False)
        test_run.tests.create(name='baz', suite=suite, result=None)
        test_run.tests.create(name='qux', suite=suite, result=False)

        summary = build.test_summary
        self.assertEqual(4, summary['total'])
        self.assertEqual(1, summary['pass'])
        self.assertEqual(2, summary['fail'])
        self.assertEqual(1, summary['missing'])
        self.assertEqual(['tests/bar', 'tests/qux'], sorted([t.full_name for t in summary['failures']['env']]))

    def test_metadata(self):
        build = Build.objects.create(project=self.project, version='1.1')
        env = self.project.environments.create(slug='env')
        build.test_runs.create(environment=env, metadata_file='{"foo": "bar", "baz": "qux"}')
        build.test_runs.create(environment=env, metadata_file='{"foo": "bar", "baz": "fox"}')

        self.assertEqual({"foo": "bar"}, build.metadata)

    def test_metadata_empty(self):
        build = Build.objects.create(project=self.project, version='1.1')
        env = self.project.environments.create(slug='env')
        build.test_runs.create(environment=env, metadata_file='{"foo": "bar"}')
        build.test_runs.create(environment=env, metadata_file='{"baz": "qux"}')

        self.assertEqual({}, build.metadata)

    def test_metadata_no_testruns(self):
        build = Build.objects.create(project=self.project, version='1.1')
        self.assertEqual({}, build.metadata)

    def test_metadata_with_testruns_with_empty_metadata(self):
        build = Build.objects.create(project=self.project, version='1.1')
        env = self.project.environments.create(slug='env')
        build.test_runs.create(environment=env)
        self.assertEqual({}, build.metadata)

    def test_metadata_list_value(self):
        build = Build.objects.create(project=self.project, version='1.1')
        env = self.project.environments.create(slug='env')
        build.test_runs.create(environment=env, metadata_file='{"foo": "bar", "baz": ["qux"]}')
        build.test_runs.create(environment=env, metadata_file='{"foo": "bar", "baz": ["qux"]}')
        self.assertEqual({"foo": "bar", "baz": ["qux"]}, build.metadata)
