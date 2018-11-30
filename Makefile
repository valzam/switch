start-server:
	python run.py

start-server-docker:
	docker run --env-file ./.env -t switch

build-protobuf:
	${PROTOC} -I protobuf --python_out=switch/pb protobuf/*.proto

build-docker:
	docker build -t switch .

test:
	pytest
