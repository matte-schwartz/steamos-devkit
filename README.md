
# Windows development: one time system configuration

Install [Chocolatey](https://chocolatey.org) first

In an Adminstrator powershell:

Install misc utilities:

- `choco install 7zip`

Install Python 3.10:

# These options install into c:\Python310 for all users
- `choco install python --version 3.10.7 --params "'/qn /norestart ALLUSERS=1 TARGETDIR=c:\Python310'"`

Python will install to C:\Python30. Restart the shell to pickup it up.

Run the following:

- `python -m pip install --upgrade pip`
- `python -m pip install --upgrade setuptools`

Install the Microsoft Visual C++ compiler, per https://wiki.python.org/moin/WindowsCompilers:

- `choco install visualstudio2019community`

Then run 'Visual Studio Installer' from the Start menu, and enable the 'Python development' workload, plus the 'Python native development tools' option.

Install cygwin with needed packages:

- `choco install cygwin --params "/InstallDir:C:\cygwin64"`
- `choco install rsync openssh --source=cygwin`

# Windows development: python virtualenv setup

Next, prepare a python virtualenv with all the necessary dependencies. This step can be repeated in fresh clones of the repositories.

From your checkout of steamos-devkit:

- setup: `python -m venv .`
- activate: `.\Scripts\Activate.ps1`

    If you get an `UnauthorizedAccess` error due to [execution policies](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies), run the following command first: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

Start by updating base tools:

- `python -m pip install --upgrade pip`
- `python -m pip install --upgrade setuptools`

Install project dependencies:

- `pip install -r requirements.txt`

You are ready for development. The application can be started by running `python .\devkit-gui.py` in the client/ directory.

# Windows packaging:

From the activated virtual env:

- `python .\setup\package-windows.py`

# Linux development:

We recommended a system with Python 3.9 or 3.10 (Arch and derivatives, or Ubuntu 20.x or newer)

Instructions below use [pipenv](https://pipenv.pypa.io/en/latest/), but can be adapted to any other python virtual environment solution.

- `pipenv shell`
- `pip install -r requirements.txt`

(Assuming you are on a Python 3.10 system, see wheels documentation below)

- `cd client`
- `./devkit-gui.py`

# Linux packaging for distribution:

## One time setup:

From a blank Ubuntu 18 (bionic) VM, or via toolbox, podman, docker etc.:

Installing 3.9, 3.10, 3.11 backports from https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa

As root:

```text
$ add-apt-repository ppa:deadsnakes/ppa
$ apt-get update
$ apt-get upgrade
$ apt-get install gcc python3.9 python3.9-dev python3.9-distutils python3.10 python3.10-dev python3.10-distutils python3.11 python3.11-dev python3.11-distutils
```

Boostrapping pip and pipenv.

As user:

```text
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3.9 ./get-pip.py
$ python3.9 -m pip install pipenv
$ python3.10 ./get-pip.py
$ python3.10 -m pip install pipenv
$ python3.11 ./get-pip.py
$ python3.11 -m pip install pipenv
```

## Package:

- Fresh git clone
- `python3.9 -m pipenv --python 3.9 shell`
- `pip install -r requirements.txt`
- `./setup/package-linux.py`

Repeat for Python 3.10 etc.
