# Issue Forwarder

A Google App Engine mini-app that receives e-mails and creates Github issues
from them.

## Setup

- copy the issueforwarder directory into your App Engine app's folder.
- configure App Engine to [receive inbound mail] (https://cloud.google.com/appengine/docs/python/mail/receivingmail)
  - the handler script should be `issueforwarder.main.app`
- create a config.yaml file in the issueforwarder directory with these keys and
  values
  - `base_url`: https://api.github.com
  - `repo_name`: the name of the repo in which to create issues
  - `repo_owner`: the github user or organisation that owns the repository
  - `auth_token`: a [personal access
token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) for the repo_owner.
    - The token's scope should be public_repo for public repositories or repo for private repositories.
  - `user_agent_string`: a [user agent string](https://developer.github.com/v3/#user-agent-required) to send in api calls

## Usage

- send/forward e-mails to some.address@your-appid.appspotmail.com
- an issue will created in github with the e-mail's subject as a title and the
  e-mail's body as the issue body text.
