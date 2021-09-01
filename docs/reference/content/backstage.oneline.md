
Back to [Reference Overview](https://github.com/pyrustic/backstage/blob/master/docs/reference/README.md#readme)

# backstage.oneline



<br>


```python
HANDLERS = {'build': <class 'backstage.handler.build_handler.BuildHandler'>, 'hub': <class 'backstage.handler.hub_handler.HubHandler'>, 'init': <class 'backstage.handler.init_handler.InitHandler'>, 'link': <class 'backstage.handler.link_handler.LinkHandler'>, 'release': <class 'backstage.handler.release_handler.ReleaseHandler'>, 'recent': <class 'backstage.handler.recent_handler.RecentHandler'>, 'relink': <class 'backstage.handler.relink_handler.RelinkHandler'>, 'run': <class 'backstage.handler.run_handler.RunHandler'>, 'target': <class 'backstage.handler.target_handler.TargetHandler'>, 'unlink': <class 'backstage.handler.unlink_handler.UnlinkHandler'>, 'version': <class 'backstage.handler.version_handler.VersionHandler'>}

```

<br>

```python

def command(line=None, target=None):
    """
    Param:
        - line is a string or a list. Example "link /home/project" or ["link", "/home/proj"]
        - target is a path string
    """

```

