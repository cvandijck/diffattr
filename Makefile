ifeq ($(OS), Windows_NT)
	MAKE_OS := Windows
else
	MAKE_OS := Linux
endif

PYTHON_VERSION = 3.9
VENV_NAME = .venv
DOCKER_TAG = diffattr

BUILD_DIR = ./_build
BUILD_WHEEL_DIR = $(BUILD_DIR)/wheel
BUILD_TEST_DIR = $(BUILD_DIR)/test

UV = uv
ifeq ($(MAKE_OS), Windows)
	PYTHON = $(VENV_NAME)\Scripts\python
	ACTIVATE = $(VENV_NAME)\Scripts\activate
else
	PYTHON = $(VENV_NAME)/bin/python
	ACTIVATE = source $(VENV_NAME)/bin/activate
endif

PIP = $(RUN_MODULE) pip

install: create-env install-project install-pre-commit activate-help

create-env:
	$(info MAKE: Initializing environment in .venv ...)
	$(UV) venv --python $(PYTHON_VERSION) $(VENV_NAME) --seed
	$(UV) pip install --upgrade "pip>=24"

install-project:
	$(info MAKE: Installing project ...)
	$(UV) sync --all-packages

upgrade-project:
	$(info MAKE: Upgrade project dependencies ...)
	$(UV) sync --upgrade --all-packages

install-pre-commit:
	$(info MAKE: Installing pre-commit hooks...)
	$(UV) run pre-commit install

activate-help:
	$(info MAKE: To activate the virtual environment, run: $(ACTIVATE))

test:
	$(info MAKE: Running tests ...)
	$(UV) run pytest tests

pre-commit:
	$(info MAKE: Pre-commit hooks check over all files...)
	$(UV) run pre-commit run --all-files

build-wheels:
	$(UV) build . --out-dir $(BUILD_WHEEL_DIR)

install-wheels:
	$(UV) pip install $(BUILD_WHEEL_DIR)/*.whl

build-docker:
	docker build -t $(DOCKER_TAG) .

run-app:
	$(PYTHON) app/app.py

run-docker:
	docker run -p 8501:8501 $(DOCKER_TAG)

publish-wheels:
	$(UV) publish $(BUILD_WHEEL_DIR)/*