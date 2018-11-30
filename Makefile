start-server:
	python run.py server

start-server-docker:
	docker run --env-file ./.env -t switch

start-producer:
	python run.py producer

build-protobuf:
	${PROTOC} -I protobuf --python_out=switch/pb protobuf/*.proto

build-docker:
	docker build -t switch .

test:
	pytest
