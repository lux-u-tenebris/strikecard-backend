#! /usr/bin/bash
# Add to cron with `crontab -e` and adding the following lines.
# This setup will run once daily at midnight, which is the recommendation.
# The script handles its own logging.
#
# Prerequisites:
#    - <YOUR_ARCHIVE_DIR> exists and is writeable (chmod u+w ...)
#    - This script is executable (chmod u+x ...)
#
# Check <YOUR_ARCHIVE_DIR> for output log files.
#
######
#
# # archive https://github.com/GS-US/strikecard-backend.git
# 0 0 * * * <YOUR_PARENT_DIR>/strikecard-backend/archive/archive.sh <YOUR_ARCHIVE_DIR>
#
######
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
