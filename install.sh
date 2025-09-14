
set -ex

# no run as root
if [ "$EUID" -eq 0 ]; then
    echo "Do not run install scripts as root."
    exit 1
fi

# dependency checks
if ! command -v git &> /dev/null; then
    # check if git is installed, and clone the repo down
    echo "Git could not be found, please install it."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Docker could not be found, please install it."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose could not be found, please install it."
    exit 1
fi

# get install dir
if [[ -f "$0" ]]; then
    install_dir="$(pwd)"
else
    install_dir="$(dirname "$0")"
fi

# go to dir
cd "$install_dir"

# clone if safe
expected_name="strikecard-backend"
if [[ -d "$expected_name" ]]; then
    cd "$expected_name"
fi

# "|| :" means execute no-op, this ensures errors from rev-parse are swallowed
repo="$(git rev-parse --show-toplevel 2> /dev/null)" || :
if [[ -z "$repo" ]]; then
    # clone the repo down
    git clone "https://github.com/GS-US/strikecard-backend.git" "$expected_name"
    cd "$expected_name"
fi

url="$(git config --get remote.origin.url)"
base="$(basename $url)"
name="${base%.*}"
if [[ "$name" != "$expected_name" ]]; then
    echo "You appear to be in a different repository:"
    echo "$repo"
    echo "Please run the script with an empty directory, or in the strikecard-backend repository."
fi

# ACTUAL INSTALLATION

# run starfish install script
./starfish/install.sh

# build the docker image
docker-compose build

# make postgres_data and chown it to nobody:nogroup
mkdir -p postgres_data
chown -R nobody:nogroup postgres_data
