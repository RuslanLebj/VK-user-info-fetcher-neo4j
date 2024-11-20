.PHONY: up down dump clean-dump

# Переменные
DOCKER_COMPOSE = docker-compose
DUMP_DIR = dump
DUMP_FILE = $(DUMP_DIR)/neo4j.dump
NEO4J_CONTAINER = vk-user-info-fetcher_neo4j_1
NEO4J_VOLUME = vk-user-info-fetcher_neo4j_data

# Запуск контейнеров
up:
	$(DOCKER_COMPOSE) up -d

# Остановка и удаление контейнеров
down:
	$(DOCKER_COMPOSE) down

# Создание дампа базы данных
dump:
	mkdir -p $(DUMP_DIR)
	docker stop $(NEO4J_CONTAINER)
	docker run --rm \
		-v $(NEO4J_VOLUME):/data \
		-v $(PWD)/$(DUMP_DIR):/dump \
		neo4j:4.3 \
		neo4j-admin dump --database=neo4j --to=/dump/neo4j.dump
	docker start $(NEO4J_CONTAINER)

# Удаление старого дампа
clean-dump:
	rm -f $(DUMP_FILE)
