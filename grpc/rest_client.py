import requests

BASE_URL = "http://127.0.0.1:5000/documents"


class CMSClient:
    
    @staticmethod
    def add_document(title,content,author,tag):
        payload = {"title": title, "content": content, "author": author,"tags":tag}
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print(response.json()["message"])
        else:
            print(f"Error: {response.json()['message']}")
            
    @staticmethod
    def list_documents(author,tags):
        payload = {"author":author,"tags":tags}
        response = requests.get(BASE_URL,params=payload)
        if response.status_code == 200:
            documents = response.json()
            if not documents:
                print("No items found.")
            else:
                print(response.json()["message"])
        else:
            print(f"Error: Unable to fetch items (Status Code: {response.status_code})")
    
    @staticmethod
    def get_document(document_id):
        response = requests.get(f"{BASE_URL}/{id}")
        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(f"Error: Unable to fetch items (Status Code: {response.status_code})")
            
    @staticmethod
    def update_document(document_id, payload):
        response = requests.put(f"{BASE_URL}/{id}", json=payload)
        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(f"Error: Unable to fetch items (Status Code: {response.status_code})")


    @staticmethod
    def delete_document(document_id):
        response = requests.delete(f"{BASE_URL}/{id}")
        if response.status_code == 204:
            return "Document deleted successfully"
        else:
            return response.status_code, response.text


if __name__ == "__main__":
    client = CMSClient()

    client.add_document("Book1", "content of book1","abc","science")
    client.add_document("Book2", "content of book2","pqr","health")
    client.add_document("Book3", "content of book3","xyz","Maths")
    client.add_document("Book4", "content of book4","xyzp","science,Maths")
    client.list_documents("","science")
