.MAKEFLAGS += --warn-undifined-variables --no-print-directory
.SHELLFALGS := -ue -o pipfail -c

all: help
.PHONY: all

# Use bash for inline if-statements
SHELL:=bash
APP_NAME=$(shell basename "`pwd`")
OWNER?=martin.krause
DOCKER_REPOSITORY=local
SOURCE_IMAGE=$(DOCKER_REPOSITORY)/$(OWNER)/$(APP_NAME)

# Enable BuildKit for Docker build
export DOCKER_BUILDKIT:=1

##@ Helpers
help: ## display this help
	@echo "$(APP_NAME)"
	@echo "============================="
	@awk 'BEGIN {FS = ":.*##"; printf "\033[36m\033[0m"} /^[a-zA-Z0-9_%\/-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@printf "\n"


##@ Versioning
bumpversion: ## Bumps the version of the project and writes the new version back to pyproject.toml
ifeq ($(shell git status --porcelain=v1 2>/dev/null | wc -l),)
	@$(eval VERSION := $(shell poetry version -s))
	@$(eval NEW_VERSION := $(shell poetry version $(notdir $@)))
	@git commit -m "$(NEW_VERSION)" pyproject.toml --quiet --no-verify
	@git tag -a $(shell poetry version -s) -m "$(NEW_VERSION)"
	@echo $(NEW_VERSION)
else
	@echo "needs update: $(shell git update-index --really-refresh | cut -d':' -f1 )"
	$(info [WARNING] Unstaged files detected.)
endif


##@ Hooks for files and images
hook: DOCS_PATH?=./docs
hook: TAGGING_CONFIG?=./.docker-tagging.yml
hook: ## run post-build hooks for an image
	# HINT: make the --version-file parameter configurable and take the value from IMAGE_TAG
	@poetry run tagging --short-image-name "$(APP_NAME)" --owner "$(DOCKER_REPOSITORY)/$(OWNER)" --wiki-path "$(DOCS_PATH)" --config "$(TAGGING_CONFIG)" --version-file


##@ Build Jupyterlab Image
build: IMAGE_TAG?=latest
build: ## build images
	docker build --rm --force-rm -t $(SOURCE_IMAGE):$(IMAGE_TAG) .


##@ Run Jupyterlab container
run: DARGS?=-e JUPYTER_ENABLE_LAB=yes
run: IMAGE_TAG?=latest
run: PORT?=8888
run: JARGS?=start-notebook.sh --NotebookApp.token="" --NotebookApp.notebook_dir=/home/jovyan/work
run: DATA_DIR?=`pwd`/data
run: ## Run container
	docker run \
	-it --rm -p $(PORT):8888 \
	-e PYTHONPATH=$(PYTHONPATH):/home/jovyan/work/src \
	-e DATA_DIR=/home/jovyan/data \
	-v $(DATA_DIR):/home/jovyan/data \
	-v $(shell pwd):/home/jovyan/work $(DARGS) \
	$(SOURCE_IMAGE):$(IMAGE_TAG) $(JARGS)


##@ Prepare mlflow directories
prepare: ## Prepare directories for logging to MLflow
	mkdir -p mlflow/mlartifacts
	mkdir -p mlflow/mlruns
	chmod -R 755 mlflow


##@ Build stack
build-compose: DARGS?=--no-cache
build-compose: ## Build composition locally
	$(MAKE) prepare
	docker-compose build $(DARGS)

##@ Build and run jupyter stack
run-jupyter: ## Run composition locally
	$(MAKE) prepare
	docker-compose --profile jupyter up --build

##@ Build and run ingestion stack
run-ingest: ## Run composition locally
	$(MAKE) prepare
	docker-compose --profile ingest up --build

##@ Build and run training stack
run-train: ## Run composition locally
	$(MAKE) prepare
	docker-compose --profile train up --build

##@ Build and run production stack
run-production: ## Run composition locally
	$(MAKE) prepare
	docker-compose --profile production up --build

##@ Build and run jupyter, ingestion, training and production stack
run-all: ## Run composition locally
	$(MAKE) prepare
	docker-compose \
	--profile jupyter \
	--profile ingest \
	--profile train \
	--profile production \
	up --build

##@ Serving a trained model using a webserver. Note: `make run-compose` must be done first!!!
serve: RUN_ID=
serve: PORT?=8001
serve: ## Serve based on run_id and port (only ports 8001 - 8009 are allowed when you want to access it locally)
	docker exec -it luxoft-modelserve ./serve-model.sh $(PORT) $(RUN_ID)
