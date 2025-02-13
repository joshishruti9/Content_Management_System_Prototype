import grpc
import todo_pb2
import todo_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = todo_pb2_grpc.CMSStub(channel)
       
        new_document = todo_pb2.Document(title="Sample Document", content="This is a sample document.", author="abc", tags=["tech", "Maths"])
        response = stub.create_document(todo_pb2.CreateItemRequest(document=new_document))
        print(response.document)
        
        response = stub.export_document(todo_pb2.ExportItemRequest(author="abc", tags=["tech"]))
        
        if response:
            print(response)
        else:
            print("No document found matching the criteria.")

if __name__ == "__main__":
    run()