from concurrent import futures
import grpc
import todo_pb2
import todo_pb2_grpc
from CSVStrategy import csv_strategy


documents = {}
strategy = "csv"
item_id_counter = 1

class CMSServicer(todo_pb2_grpc.CMSServicer):
        
    def create_document(self, request, context):
        global item_id_counter
        document = request.document
        document.id = str(item_id_counter)
        item_id_counter += 1
        documents[document.id] = document
        return todo_pb2.CreateItemResponse(document=document)
        
    def export_document(self,request,context):
        print(f"Received request: Author = {request.author}, Tags = {request.tags}")
        author = request.author
        tags = request.tags
        
        filtered_documents = []
        
        for document in documents.values():
            if author and tags:
                if document.author == author and any(tag in document.tags for tag in tags):
                    filtered_documents.append(document)
            elif author:
                if document.author == author:
                    filtered_documents.append(document)
            elif tags:
                if all(tag in document.tags for tag in tags):
                    filtered_documents.append(document)
            else:
                filtered_documents.append(document)
                
        print(f"filtered_documents:{filtered_documents}")
    
        csv_strategy.export(filtered_documents)
         
        return todo_pb2.ExportItemResponse(document=filtered_documents)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_CMSServicer_to_server(CMSServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()