# #!/usr/bin/env python
# -*- coding: utf-8 -*-

from .responses import (token_from_oauth1,
                        disable_access_token,
                        account_info,
                        get_token,
                        get_delta,
                        sandbox,
                        get_media,
                        put_file,
                        get_file,
                        delete_file,
                        move_file,
                        metadata)

# the (\d+) parameter in urls is the api version info

url_paths = [{'https://api.dropbox.com/(\d+)/oauth2/token_from_oauth1$':
                  token_from_oauth1},
             {'https://api.dropbox.com/(\d+)/disable_access_token':
                  disable_access_token},
             {'https://api.dropbox.com/(\d+)/account/info':
                  account_info},
             {'https://api.dropbox.com/(\d+)/oauth2/token':
                  get_token},
             {'https://api.dropbox.com/(\d+)/delta':
                  get_delta},
             {'https://api.dropbox.com/(\d+)/metadata/sandbox':
                  sandbox},
             {'https://api.dropbox.com/(\d+)/media/([a-zA-Z]+)/([a-zA-Z]+)':
                  get_media},
             {'https://api-content.dropbox.com/(\d+)/files_put/([a-zA-Z]+)/([a-zA-Z]+)':
                  put_file},
             {'https://api-content.dropbox.com/(\d+)/files/([a-zA-Z]+)/([a-zA-Z]+)':
                  get_file},
             {'https://api.dropbox.com/(\d+)/fileops/delete$':
                  delete_file},
             {'https://api.dropbox.com/(\d+)/fileops/move$':
                  move_file},
             {'https://api.dropbox.com/(\d+)/metadata/([a-zA-Z]+)/([a-zA-Z]+)':
                  metadata},]

