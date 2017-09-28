PYTHON_CMD="python"
PIP_CMD="pip"

PYTHON_VERSION=$($PYTHON_CMD --version | cut -d\  -f 2 | cut -d. -f 1)
if [ "$PYTHON_VERSION" != "3" ]; then
	PYTHON_CMD="python3"
	PYTHON3_VERSION=$($PYTHON_CMD --version | cut -d\  -f 2 | cut -d. -f 1)

	if [ "$PYTHON3_VERSION" != "3" ]; then
		echo "PYTHON 3 not found"
		echo "Please install pyton3 & pip"
		exit 1
	fi
fi

PIP_VERSION=$($PIP_CMD --version | cut -d\  -f 6 | cut -d. -f 1)
if [ "$PIP_VERSION" != "3" ]; then
	PIP_CMD="pip3"
	PIP3_VERSION=$($PIP_CMD --version | cut -d\  -f 6 | cut -d. -f 1)

	if [ "$PIP3_VERSION" != "3" ]; then
		echo "pip for python 3 not found"
		echo "Please install pip for python3"
		exit 1
	fi
fi

echo "Install dependencies"

# install on pip only
sudo $PIP_CMD install Django
sudo $PIP_CMD install Pillow
# init data base
$PYTHON_CMD ./manage.py makemigrations
$PYTHON_CMD ./manage.py migrate
$PYTHON_CMD ./manage.py loaddata backend/fixtures/database.json

