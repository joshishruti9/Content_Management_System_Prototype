import multiprocessing
import subprocess

if __name__ == "__main__":
    
    # Start REST API in a separate process
    rest_serve = multiprocessing.Process(target=subprocess.run(["python", "rest_server.py"]))
    grpc_serve = multiprocessing.Process(target=subprocess.run(["python", "grpc_server.py"]))
    
    rest_serve.start()
    grpc_serve.start()

    # Wait for both processes to finish
    rest_serve.join()
    grpc_serve.join()