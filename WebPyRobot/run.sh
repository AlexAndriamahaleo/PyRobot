PYTHON_CMD="python"

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

$PYTHON_CMD manage.py runserver
