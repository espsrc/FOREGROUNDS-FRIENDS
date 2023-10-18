# Software requirements

This notebook makes use of the following software:

* Python 3.7+
* sextractor

# Installation instructions

The following instructions have been tested on a clean Ubuntu system, but should also work on a Mac. Root permissions are not required. Windows is not supported.

1. Install Homebrew, by downloading it from the official repository and running the installation script. Run the following commands in a shell:

```
git clone https://github.com/Homebrew/brew homebrew
eval "$(homebrew/bin/brew shellenv)"
brew update --force --quiet
chmod -R go-w "$(brew --prefix)/share/zsh"
```

2. If Homebrew was installed with root permissions, skip this step and go to step 3. If root isn't available, we need to manually add the Homebrew directories to PATH, by appending these two lines at the end of ~/.bashrc:

```
export PATH=$PATH:/home/andres/homebrew/bin
export PATH=$PATH:/home/andres/homebrew/sbin
```

Finally, restart the shell (`exec bash`, or `exec zsh` on Mac).

3. Install Python: `brew install python3`.

4. Install the required Python libraries: `pip3 install numpy astropy Pillow matplotlib`.

5. Install sextractor: `brew install sextractor`.


