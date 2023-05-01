## Welcome to dependency-metrics ##

### Summary
A command line tool to analyze and monitor how up-to-date dependencies of a project are. For more detail, see the [Usage](#usage) section below.

#### Supported Package Managers
- pip
- yarn

#### Supported Application Monitoring Platforms
- DataDog


### Usage
Run the `dependency-metrics` tool from within the repository you wish to generate metrics for.

#### Default behavior

All that is needed is the package manager you want to generate metrics for, and `dependency-metrics` will output a table detailing
how out-of-date each dependency is.

```commandline
$ dependency-metrics pip
Behind   Package                      Latest       Version
0.1.0    my-depedency                 1.1.0        1.0.0
2.0.0    my-other-dependency          3.2.1        1.2.3
```

#### --stats option

Use the `--stats` option to generate a simple dictionary that displays the total number of outdated dependencies, as well as a breakdown detailing the number of outdated dependencies for each version type.

```commandline
$ dependency-metrics pip --stats
Outdated: 1
Multi-Major: 1
Major: 0
Minor: 1
Patch: 0
Unknown: 0
```

#### --send option

> **NOTE:**  Additional setup is required to successfully post stats to a supported backend. See [platform setup](#application-monitoring-platform-setup) for further information.

Use the `--send` option to post the same metrisc generated by `--stats` to an application monitoring platform.

```commandline
$ dependency-metrics pip --send
```

### Application Monitoring Platform Setup
This is required to make use of the `--send` option, enabling the ability to send generated stats to a backend of your choice.

#### DataDog
Set the `DATADOG_API_KEY` and `DATADOG_APP_KEY` environment variables in the environment you will run `dependency-metrics <package_manager> --send` from.

### Development

#### Requirements

```commandline
pip install -e .  # installs dependencies defined in pyproject.toml
pip install -e .[test]  # installs test dependencies -- '.[test]' if using zsh
```

#### Tests
Must install test dependencies first. See [requirements](#requirements) above.

```commandline
nose2  # runs all tests
nose2 dot.path.to.file.class.or.test  # runs specific test
```
