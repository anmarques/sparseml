.PHONY: build docs test

BUILDDIR := $(PWD)
CHECKDIRS := integrations src tests utils setup.py
CHECKGLOBS := 'integrations/**/*.py' 'src/**/*.py' 'tests/**/*.py' 'utils/**/*.py' setup.py
DOCDIR := docs
MDCHECKGLOBS := 'docs/**/*.md' 'docs/**/*.rst' 'integrations/**/*.md'
MDCHECKFILES := CODE_OF_CONDUCT.md CONTRIBUTING.md DEVELOPING.md README.md
SPARSEZOO_TEST_MODE := "true"

BUILD_ARGS :=  # set nightly to build nightly release
TARGETS := ""  # targets for running pytests: deepsparse,keras,onnx,pytorch,pytorch_models,pytorch_datasets,tensorflow_v1,tensorflow_v1_models,tensorflow_v1_datasets
PYTEST_ARGS ?= ""
ifneq ($(findstring deepsparse,$(TARGETS)),deepsparse)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/deepsparse
endif
ifneq ($(findstring keras,$(TARGETS)),keras)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/keras
endif
ifneq ($(findstring onnx,$(TARGETS)),onnx)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/onnx
endif
ifneq ($(findstring pytorch,$(TARGETS)),pytorch)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/pytorch
endif
ifneq ($(findstring pytorch_models,$(TARGETS)),pytorch_models)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/pytorch/models
endif
ifneq ($(findstring pytorch_datasets,$(TARGETS)),pytorch_datasets)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/pytorch/datasets
endif
ifneq ($(findstring tensorflow_v1,$(TARGETS)),tensorflow_v1)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/tensorflow_v1
endif
ifneq ($(findstring tensorflow_v1_models,$(TARGETS)),tensorflow_v1_models)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/tensorflow_v1/models
endif
ifneq ($(findstring tensorflow_v1_datasets,$(TARGETS)),tensorflow_v1_datasets)
    PYTEST_ARGS := $(PYTEST_ARGS) --ignore tests/sparseml/tensorflow_v1/datasets
endif

# run checks on all files for the repo
quality:
	@echo "Running copyright checks";
	python utils/copyright.py quality $(CHECKGLOBS) $(MDCHECKGLOBS) $(MDCHECKFILES)
	@echo "Running python quality checks";
	black --check $(CHECKDIRS);
	isort --check-only $(CHECKDIRS);
	flake8 $(CHECKDIRS);

# style the code according to accepted standards for the repo
style:
	@echo "Running copyrighting";
	python utils/copyright.py style $(CHECKGLOBS) $(MDCHECKGLOBS) $(MDCHECKFILES)
	@echo "Running python styling";
	black $(CHECKDIRS);
	isort $(CHECKDIRS);

# run tests for the repo
test:
	@echo "Running python tests";
	SPARSEZOO_TEST_MODE="true" pytest tests $(PYTEST_ARGS)

# create docs
docs:
	@echo "Running docs creation";
	export SPARSEML_IGNORE_TFV1="True"; python utils/docs_builder.py --src $(DOCDIR) --dest $(DOCDIR)/build/html;

docsupdate:
	@echo "Runnning update to api docs";
	find $(DOCDIR)/api | grep .rst | xargs rm -rf;
	export SPARSEML_IGNORE_TFV1="True"; sphinx-apidoc -o "$(DOCDIR)/api" src/sparseml;

# creates wheel file
build:
	python3 setup.py sdist bdist_wheel $(BUILD_ARGS)

# clean package
clean:
	rm -fr .pytest_cache;
	rm -fr docs/_build docs/build;
	find $(CHECKDIRS) | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -fr;
