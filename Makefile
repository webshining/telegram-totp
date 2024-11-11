-include .env
LOCALES_PATH := ./data/locales
I18N_DOMAIN := $(or $(I18N_DOMAIN),bot)
SURREAL_USER := $(or $(SURREAL_USER),root)
SURREAL_PASS := $(or $(SURREAL_PASS),root)
SURREAL_NS := $(or $(SURREAL_NS),bot)
SURREAL_DB := $(or $(SURREAL_DB),bot)

.PHONY: logs

bot:
	python main.py
server:
	uvicorn server:app --reload --host 0.0.0.0 --port 80
logs:
	docker compose logs -f app
rebuild:
	docker compose up -d --no-deps --force-recreate --build
pybabel_extract:
	pybabel extract --input-dirs=. -o $(LOCALES_PATH)/$(I18N_DOMAIN).pot
pybabel_init: 
	pybabel init -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d $(LOCALES_PATH) -D $(I18N_DOMAIN) -l en && \
	pybabel init -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d $(LOCALES_PATH) -D $(I18N_DOMAIN) -l ru && \
	pybabel init -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d $(LOCALES_PATH) -D $(I18N_DOMAIN) -l uk
pybabel_update: 
	pybabel update -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d ./data/locales -D $(I18N_DOMAIN)
pybabel_compile:
	pybabel compile -d $(LOCALES_PATH) -D $(I18N_DOMAIN)
db_export:
	docker compose exec db //surreal export --conn http://localhost:8000 --user $(SURREAL_USER) --pass $(SURREAL_PASS) --ns $(SURREAL_NS) --db $(SURREAL_DB) export.surql && \
	docker compose cp db:/export.surql ./
db_import:
	docker compose cp ./export.surql db:/export.surql && \
	docker compose exec db /surreal import --conn http://localhost:8000 --user $(SURREAL_USER) --pass $(SURREAL_PASS) --ns $(SURREAL_NS) --db $(SURREAL_DB) export.surql