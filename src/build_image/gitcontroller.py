import json
import os
import shutil
import subprocess
from io import BytesIO
from urllib.parse import urlencode
import git
import pycurl


class GitController:
    def __init__(self, oauth_key: str, oauth_secret: str):
        self.oauth_key = oauth_key
        self.oauth_secret = oauth_secret
        self.oauth_url = 'https://bitbucket.org/site/oauth2/access_token'
    
    def clone(self, repository: str, tag: str, path: str):
        response_buffer = BytesIO()
        c = pycurl.Curl()
        post_data = {'grant_type': 'client_credentials'}
        postfields = urlencode(post_data)
        c.setopt(c.URL, self.oauth_url)
        c.setopt(c.POSTFIELDS, postfields)
        c.setopt(c.USERPWD, self.oauth_key + ':' + self.oauth_secret)
        c.setopt(c.WRITEFUNCTION, response_buffer.write)
        try:
            c.perform()
            c.close()
            body = response_buffer.getvalue()
            repo_json = json.loads(body)
        except pycurl.error as e:
            print(e)
            return None
        else:
            access_token = repo_json["access_token"]
            url = "https://x-token-auth:{}@bitbucket.org/latonaio/{}.git".format(
                access_token, repository)
            try:
                if os.path.exists(path):
                    shutil.rmtree(path)
                return git.Repo.clone_from(url, path, branch=tag)
            except Exception as e:
                print(e)
                return None
