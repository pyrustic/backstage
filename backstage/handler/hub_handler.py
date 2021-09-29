import os
import os.path
import backstage
from backstage.core.funcs import create_kurl
from shared import Jason


class HubHandler:
    """
    Description
    -----------
    Use this command to retrieve useful information
    from a Github repository.

    Usage
    -----
    - Description: Retrieve useful information from
    this repository https://github.com/pyrustic/demo
    - Command: hub pyrustic/demo
    """
    def __init__(self, target, app_pkg, *args):
        self._target = target
        self._app_pkg = app_pkg
        self._args = args
        self._process(args)

    def _process(self, args):
        if not args:
            cache = self._default_owner_repo()
            if cache:
                text = "{}/{}".format(*cache)
                args = [text]
            else:
                print("Wrong usage. Check 'help hub'.")
                return
        elif len(args) > 1:
            print("Wrong usage. Check 'help hub'.")
            return
        owner_repo = args[0].split("/")
        if len(owner_repo) != 2:
            print("Incorrect request. Check 'help hub'.")
            return
        owner, repo = owner_repo
        print("https://github.com/{}/{}\n".format(owner, repo))
        gurl = create_kurl()
        if not self._show_repo_description(gurl, owner, repo):
            return
        if not self._show_latest_release(gurl, owner, repo):
            return
        if not self._show_latest_releases_downloads(gurl, owner, repo):
            return

    def _show_repo_description(self, gurl, owner, repo):
        cache = backstage.github_repo_description(gurl, owner, repo)
        status_code, status_text, data = cache
        if status_code not in (200, 304):
            print("Failed to get the repo description")
            if status_code:
                print("{} {}".format(status_code, status_text))
            else:
                print(status_text)
            return False
        self._show_section("Repository description")
        description = data["description"]
        description = "- No description -" if not description else description
        print(description)
        print("Created on {}".format(data["created_at"]))
        stargazers = data["stargazers_count"]
        subscribers = data["subscribers_count"]
        print("{} Stargazer{} and {} Subscriber{}".format(stargazers,
                                                          self._plural(stargazers),
                                                          subscribers,
                                                          self._plural(subscribers)))
        print("")
        return True

    def _show_latest_release(self, gurl, owner, repo):
        cache = backstage.github_latest_release(gurl, owner, repo)
        status_code, status_text, data = cache
        if status_code not in (200, 304):
            print("Failed to get the latest release info")
            if status_code:
                print("{} {}".format(status_code, status_text))
            else:
                print(status_text)
            return False
        self._show_section("Latest release")
        print("Tag name: {}".format(data["tag_name"]))
        print("Published on {}".format(data["published_at"]))
        downloads = data["downloads_count"]
        print("{} Download{}".format(downloads,
                                     self._plural(downloads)))
        print("")
        return True

    def _show_latest_releases_downloads(self, gurl, owner, repo):
        cache = backstage.github_downloads(gurl, owner, repo)
        status_code, status_text, data = cache
        if status_code not in (200, 304):
            print("Failed to get the latest ten (pre)releases info")
            if status_code:
                print("{} {}".format(status_code, status_text))
            else:
                print(status_text)
            return False
        self._show_section("Latest ten (pre)releases")
        downloads = data
        print("{} Download{}".format(downloads,
                                     self._plural(downloads)))
        print("")
        return True

    def _show_section(self, title):
        count = len(title)
        print(title)
        print("".join(["=" for _ in range(count)]))

    def _plural(self, item):
        item = int(item)
        return "s" if item > 1 else ""

    def _default_owner_repo(self):
        if not self._target and not self._app_pkg:
            return None
        backstage_data_path = os.path.join(self._target, self._app_pkg,
                                            "pyrustic_data", "backstage",
                                            "data")
        github_release_form = os.path.join(backstage_data_path,
                                           "github_release_form.json")
        if not os.path.exists(github_release_form):
            return None
        jason = Jason("github_release_form.json", location=backstage_data_path)
        if not jason.data:
            return None
        owner = jason.data["owner"]
        repo = jason.data["repository"]
        if not owner or not repo:
            return None
        return owner, repo
