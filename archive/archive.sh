#! /usr/bin/bash

help="Repo archival script.

The only input is an existing, absolute path to a directory (<YOUR_ARCHIVE_DIR>)
where outputs are written. Output names are prefixed with the current time. The
script handles its own logging, which is also put into the output as a text
file.

## Manual Usage

# ensure you are in the <REPO_DIR>
archive/archive.sh <YOUR_ARCHIVE_DIR>

# see help message
archive/archive.sh

## Crontab Usage

Add to cron with 'crontab -e' and adding the lines in 'Example Crontab Entry'
below. The example setup will run once daily at midnight.

Prerequisites:
  - The repo is cloned onto your system at <REPO_DIR> (git clone ...).
  - <YOUR_ARCHIVE_DIR> exists and is writeable (chmod u+w ...).
  - This script is executable (chmod u+x ...).

Check <YOUR_ARCHIVE_DIR> for output log files and ensure the script runs as
expected.

### Example Crontab Entry

# archive https://github.com/GS-US/strikecard-backend.git
0 0 * * * <REPO_DIR>/archive/archive.sh <YOUR_ARCHIVE_DIR>"

##### HELP
if [ "$#" -ne 1 ]; then
  echo "$help"
  exit 1
fi

##### GET INTO THE SCRIPT ENVIRONMENT
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

##### SETUP
output_directory="$1"
if [ ! -d "$output_directory" ]; then
  echo "does not exist: $output_directory"
  echo "please use an absolute path to an already existing directory"
  exit 1
fi

repo_url="https://github.com/GS-US/strikecard-backend"
now="$(date +"%Y-%m-%dT%H:%M:%S.%N")"
log_file="$output_directory/$now-repo.log"
touch "$log_file"
echo "Starting repo archive process." \
  >> "$log_file" 2>&1

##### GITHUB TAR DOWNLOAD

# DOWNLOAD GitHub Project representation
download_url="$repo_url/archive/refs/heads/main.tar.gz"
download_file="$output_directory/$now-github-repo.tar.gz"
wget "$download_url" \
  --output-document="$download_file" \
  >> "$log_file" 2>&1

echo "Full repository archive downloaded to: $download_file" \
  >> "$log_file" 2>&1

##### GIT CLONE TAR

# DOWNLOAD git clone representation
clone_url="$repo_url.git"
clone_dir="$output_directory/$now-clone-repo/"
clone_file="$output_directory/$now-clone-repo.tar.gz"
git clone --mirror \
  "$clone_url" "$clone_dir/.git" \
  >> "$log_file" 2>&1

# Ensure we get the full history as a mirror.
# Have to convert the mirror to
# See: https://archive.kernel.org/oldwiki/git.wiki.kernel.org/index.php/Git_FAQ.html#How_do_I_clone_a_repository_with_all_remotely_tracked_branches.3F
working_directory="$(pwd)"
cd "$clone_dir"
git config --bool core.bare false \
  >> "$log_file" 2>&1
git checkout main \
  >> "$log_file" 2>&1
cd "$working_directory"

tar -czvf "$clone_file" -C "$clone_dir" . \
  >> "$log_file" 2>&1
rm -rf "$clone_dir" \
  >> "$log_file" 2>&1
echo "Full clone downloaded to: $clone_file" \
  >> "$log_file" 2>&1
