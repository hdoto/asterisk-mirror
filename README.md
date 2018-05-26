# Asterisk Mirror

This module is an application to execute Asterisk Mirror.

## Install

```
$ pip3 install asterisk-mirror-1.0.0.tar.gz
```

## Execute

```
$ asterisk-mirror
```

## Develop environment

```
$ cd asterisk-mirror/
$ python3 -m venv envs
$ source envs/bin/activate
(envs) $ python setup.py develop
(envs) $ pip install -e .[develop]
```

### Execute module

```
(envs) $ python asterisk_mirror/main.py
```

### Test modules

```
(envs) $ python setup.py test
```

### Create distribution file

```
(envs) $ python setup.py sdist
```
