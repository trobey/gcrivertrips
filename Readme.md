# Grand Canyon river trip simulator

While a river trip simulator cannot capture all the dynamics of different groups of people traveling down the Colorado River in the Grand Canyon it can give a feel for how different scenarios compare.  In this simulator each group has a randomly generated plan of camps.  If someone already occupies the planned camp they travel to the next camp.  This is indicated in the console window where the trip simulator is started.  The river trip simulator keeps track of contacts that have to happen when a group is camping behind another group and then camps past that group the following night.  It does not try to count casual contacts when the group order remains the same such as would occur at a popular attraction.  So the actual contacts will be higher.

The model allows changing the number of private and commercial trips that launch each day and their respective trip lengths.  It also allows setting the number of days for the simulator to run.  It also allows changing whether camps adjacent to the Hualapai reservation are used to evaluate how that affects the groups traveling in the model.  For those that want to dive into the code there are many more possibilities.

The GPS waypoints in the model originally came from www.paddleon.net although they may be modified for use in the model.  River miles are displayed in blue, camps in a sand color, rapids in purple and the groups in green.  The name of the camp is displayed when a group occupies it.  This gives a sense of just how many groups are along the river corridor.  The console logs when groups are bumped from a camp and which camps they try before finding an unoccupied camp.

The model is written using Python Mesa.  Python will need to be installed on your computer.

## Installing Python

Detailed instuctions for installing Python on various operating systems can be found on the web.  The following are brief instructions.

### Windows

* Go to https://www.python.org/downloads/windows.  Find the 32 bit or 64 bit executable installer for Python 3 and download it.  There is a bug in Python 3.8 which caused problems last time it was checked.
* Run the installer.  Make sure to check to add Python to the path.  You may get a message to disable the path length limit.  Select this if it appears.
* Type python —version to verify install.
* Launch from a terminal by typing python. 

PIP is included with Python 3.4+.  Check by typing pip —version. 

### Linux

Python comes already installed on Linux.  Although Python 2 is no longer supported check by typing

* python —version
* python3 —version

If the default version is Python 2 then you may need to use python3 and pip3 instead of just python and pip.

### MacOS

Python is installed on a Mac but this is for the system to use.  Leave this alone to avoid breaking things.  Homebrew will be used.  It is a package manager for Macs.  First, Xcode will need to be installed.  It can be found in the app store.  It is a large download.   Once Xcode is installed, then open up a terminal

* /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)”

Then install Python

* brew install python3

Check to verify installation

* python —version

## Installing Python Mesa

* pip install mesa

Alternatively you can run the following which lists mesa as a requirement to be installed.

* pip install -r requirements.txt

## To run model

Type "mesa runserver" in this directory.  Press Start to run the model.  Press Step to advance each group one day in the model.
