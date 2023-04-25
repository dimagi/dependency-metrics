## Package Managers

### Adding support for new package managers
Outside this module, the only method that should be needed is
`package_metrics.package_managers.utils.get_packages`. This method handles 
translating a package manager identifier (e.g., `yarn`, `pip`, etc) into a 
list of package version info for each package installed.

This means when adding a new package manager, the method that `get_packages` 
calls (recommended to be named `get_<package_manager>_packages`), should return
a list of dictionaries in like the following:
```
[
    {"name": "test", "version": "1.0.4", "latest_version": "1.2.3"},
]
```

#### Unknown latest version
If obtaining the latest version of an installed package could potentially 
result in an unknown result, use the string `unknown` to represent the 
`latest_version` in the package version info dictionary. See 
`package_metrics.package_managers.yarn.get_yarn_packages` for an example. The 
result should look like:
```
[
    {"name": "test", "version": "2.0", "latest_version": "unknown"},
]
```
