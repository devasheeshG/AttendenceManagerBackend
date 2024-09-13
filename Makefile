SERVICE_NAME = srm-attendance-api
SERVICE_FILE = $(CURDIR)/gunicorn.service
TARGET_SERVICE_FILE = /etc/systemd/system/$(SERVICE_NAME).service
WORK_DIR = /Users/sharmayank/Documents/AttendenceManager-Backend
VENV_DIR = $(WORK_DIR)/.venv

.PHONY: all install enable start status logs stop disable clean deps database start_dev_server deploy dev format

all: dev

deps:
	@echo "Installing dependencies ..."
	poetry install

database:
	@echo "Upgrading database..."
	poetry run alembic upgrade head

start_dev_server:
	@echo "Starting development server ..."
	poetry run uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload

install:
	@echo "Installing $(SERVICE_NAME) service ..."
	@sudo cp $(SERVICE_FILE) $(TARGET_SERVICE_FILE)
	@sudo systemctl daemon-reload

enable:
	@echo "Enabling $(SERVICE_NAME) service ..."
	@sudo systemctl enable $(SERVICE_NAME).service

start:
	@echo "Starting $(SERVICE_NAME) service ..."
	@sudo systemctl start $(SERVICE_NAME).service

status:
	@echo "Checking status of $(SERVICE_NAME) service ..."
	@sudo systemctl status $(SERVICE_NAME).service

logs:
	@echo "Displaying logs for $(SERVICE_NAME) service ..."
	@sudo journalctl -u $(SERVICE_NAME).service -e

stop:
	@echo "Stopping $(SERVICE_NAME) service ..."
	@sudo systemctl stop $(SERVICE_NAME).service

disable:
	@echo "Disabling $(SERVICE_NAME) service ..."
	@sudo systemctl disable $(SERVICE_NAME).service

clean: stop disable
	@echo "Cleaning up $(SERVICE_NAME) service ..."
	@sudo rm -f $(TARGET_SERVICE_FILE)
	@sudo systemctl daemon-reload

format:
	@echo "Formatting code ..."
	poetry run black --line-length 100 --skip-string-normalization --skip-magic-trailing-comma --target-version py39 app

deploy: deps database install start

dev: deps database start_dev_server