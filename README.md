Please use following commands for both GRPC and REST API calls before API specific commands below
1. Download the project folder
2. Unzip the project folder
3. Go to project directory
4. Open command prompt

Please use following commands only for GRPC API calls
1. Run GRPC server with following commands:
   1.1 python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto
   1.2 python grpc_server.py
2. Run grpc client with following command:
   2.1 python grpc_client.py
3. This will export the CSV document

Please use following commands only for REST API calls
1. Run REST server with following command:
   1.1 python rest_server.py
2. Run REST client with following command:
   2.1 python rest_client.py

REST API calls can also be tried from browser using Swagger at http://localhost:5000/apidocs/#/Documents
