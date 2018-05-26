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

### Exec

```
(envs) $ python asterisk_mirror/main.py
```

### Test

```
(envs) $ python setup.py test
```

### Docs (experimental)

```
(envs) $ pip install -e .[docs]
(envs) $ python setup.py build_doc
```

### Create dist-file

```
(envs) $ python setup.py sdist
```
