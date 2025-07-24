# Github Archival Scripts

By default, the script is able to obtain a repo tar file from <github.com>, as well as tar a local `git clone --mirror`. The script takes one argument, the path to your desired output directory.

## Setting up a `cron` job

Add the following to your `cron`. Replace `<YOUR_PARENT_DIR>` with the parent directory of the local repository. Replace `<YOUR_ARCHIVE_DIR>` with the directory you want to archive to, which must exist for the script to function.

The script handles its own logging and working directory, so you do not need to add these to the cron file line.

```bash
# archive https://github.com/GS-US/strikecard-backend.git
0 0 * * * <YOUR_PARENT_DIR>/strikecard-backend/archive/archive.sh <YOUR_ARCHIVE_DIR>
```
