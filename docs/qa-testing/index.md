# Quality Assurance Testing

The Quality Assurance Testing section contains documentation and guides for how to install and use the system on your local machine.

These guides assume you have a basic understanding of Linux-style command lines. If you are on MacOS or Windows, there are guides below for configuring your system to make a Linux command line available to you.

If you wish to also contribute fixes for bugs, please see our [Development Section](../development/index.md).

## Strike Card Installation

Installation currently requires that you understand how to use the Linux command line to run basic commands. You'll first need to download the install file from <https://github.com/GS-US/strikecard-backend/raw/refs/heads/main/install.sh>.

If you are on Windows or MacOS, you will also need to configure your system to allow installation, then return to the Linux section.

<div class="grid cards" markdown>

- :fontawesome-brands-windows: [**Windows**](#install-on-windows)
- :fontawesome-brands-windows: [**MacOS**](#install-on-macos)
- :fontawesome-brands-linux: [**Linux**](#install-on-linux)

</div>

### Install on Windows

The easiest option is to use [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install). When you have it installed, proceed to [Install on Linux](#install-on-linux) to install the Strikecard Backend on your computer.

### Install on MacOS

TBD - If you have an Apple computer, contact us in the Discord and we can help you get configured. This will also help us add to the documentation.

### Install on Linux

Before running the installer, you'll need to install some dependencies.

- [Install Git](https://git-scm.com/downloads/linux).
    - Most distributions of Linux come with Git pre-installed.
    - Verify installation by running `git --version`.
- [Install Docker](https://docs.docker.com/engine/install/).
    - Docker Compose is also required, and installed using the instructions at the above "Install Docker" link.

Once the above dependencies are installed, your computer is ready to install the Starfish project. Please follow the instructions below.

1. Navigate to the directory you wish to use for installation. Make a note of this directory.
    - `cd $YOUR_SELECTED_DIRECTORY`
1. Download the install file.
    - `wget https://github.com/GS-US/strikecard-backend/raw/refs/heads/main/install.sh`
1. Change permissions on the install file you downloaded.
    - `chmod u+x install.sh`
1. Run the installer.
    - `./install.sh`

Next, learn about how to setup and run the Django server in the [Starting and Running the Strike Card Server Locally Section](#starting-and-running-the-strike-card-server-locally).

## Starting and Running the Strike Card Server Locally

Before testing, be sure you've [Installed Starfish](#strike-card-installation).

Each time you start a session you'll need to be sure the server is running. To test if the server is running, navigate to <https://localhost:8000> in your browser. If you reach a page with "The General Strike", the server is already running and you do not need to start it. If so, please skip to the end of this section.

Otherwise, to start the server, run `docker run app`. Doing so will cause the server to run in the foreground of the current terminal and block input. Any additional commands will need to run in a separate terminal.

Either way, please continue to the [Testing Section](#testing-the-strike-card-server).

## Testing the Strike Card Server

To get started testing, you'll first need to [Install Starfish](#strike-card-installation) and [Start the Server](#starting-and-running-the-strike-card-server-locally). Once those steps are done, proceed with the following instructions.

1. Open the server's web page on your local computer.
    - URL: <https://localhost:8000>
1. Perform tests as directed by the testing instructions.
    - [Overview](https://drive.proton.me/urls/80CBPE161C#DWR3C88Fbkhg)
    - [Plan](https://drive.proton.me/urls/E4DZGACKH8#3Xe9b4vkyzIM)

### Logging in as Admin

Some tests may require you to log in as an admin. To do so, please follow the instructions below.

1. Open the server's admin web page on your local computer.
    - URL: <https://localhost:8000/admin>
1. Log in using the default credentials.
    - Username: `admin`
    - Password: `a`
