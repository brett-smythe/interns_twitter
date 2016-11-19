# Interns Twitter

Worker service to pull tweet data and add it to [Eleanor](https://github.com/brett-smythe/eleanor).

To see how this fits in with the other repos please see [Aquatic Services Wiki](https://github.com/brett-smythe/ansible_configs/wiki)

## Install
I would recommend installing and running interns-twitter within a virtualenv.

```
python setup.py install
```

### External Dependencies
interns-twitter depends on having:
* a running instance of [Eleanor](https://github.com/brett-smythe/eleanor) setup
* Network access to Twitter's API

## Usage
interns-twitter can be invoked after the above prerequisite are met with
```
interns-twitter
```
However I would recommend running this with some sort of process managing service like supervisor
