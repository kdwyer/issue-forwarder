import unittest

from . import issues


class InboundMessageStub(object):

    """
    Stub InboundEmailMessage class.

    (google.appengine.api.mail.InboundEmailMessage)

    """

    def __init__(self):
        self.subject = u'It doesn\'t work'

    def bodies(self, content_type):
        return iter([(u'plain/text', EncodedPayloadStub())])


class EncodedPayloadStub(object):

    """
    Stub EncodedPayload class.

    (google.appengine.api.mail.EncodedPayload)

    """

    def decode(self):
        return u'I clicked on the button but nothing happened.'


class ExtractIssueTitleTestCase(unittest.TestCase):

    def setUp(self):
        self.inbound_message = InboundMessageStub()

    def test_extracts_issue_title(self):
        expected = u'It doesn\'t work'
        result = issues.extract_issue_title(self.inbound_message)
        self.assertEqual(expected, result)


class ExtractIssueBodyTestCase(unittest.TestCase):

    def setUp(self):
        self.inbound_message = InboundMessageStub()

    def test_extracts_issue_body(self):
        expected = u'I clicked on the button but nothing happened.'
        result = issues.extract_issue_body(self.inbound_message)
        self.assertEqual(expected, result)

    def test_decodes_issue_body(self):
        # A real InboundEmailMessage returns an object which returns
        # a string when decode() is called on it.
        result = issues.extract_issue_body(self.inbound_message)
        self.assertTrue(
                isinstance(result, unicode),
                'Expected unicode, got {}'.format(type(result)))


class CreatePayloadTestCase(unittest.TestCase):

    def test_creates_payload(self):
        expected = {'title': 'issue title', 'body': 'issue body'}
        result = issues.create_payload('issue title', 'issue body')
        self.assertEqual(expected, result)


class CreateURLTestCase(unittest.TestCase):
    
    def test_creates_url(self):
        expected = 'https://api.github.com/repos/kdwyer/issue-mailer/issues'
        config = {
                'repo_owner': 'kdwyer',
                'repo_name': 'issue-mailer',
                'base_url': 'https://api.github.com'
        }
        result = issues.create_url(config)
        self.assertEqual(expected, result)


class CreateHeadersTestCase(unittest.TestCase):

    def test_creates_headers(self):
        expected = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token abcdef',
                'Content-Type': 'application/json',
                'User-Agent': 'kdwyer-issue-mailer'
        }
        config = {
                'auth_token': 'abcdef',
                'user_agent_string': 'kdwyer-issue-mailer'
        }
        result = issues.create_headers(config)
        self.assertEqual(expected, result)
