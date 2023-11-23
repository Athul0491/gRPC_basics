import greet_pb2_grpc
import greet_pb2
import time
import grpc

def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or press enter to finish): ")
        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(name=name, greeting="hello")
        yield hello_request
        time.sleep(1)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. SayHello - Unary RPC")
        print("2. ParrotSaysHello - Server Side Streaming RPC")
        print("3. ChattyClientSaysHello - Client Side Streaming RPC")
        print("4. InteractingHello - Bidirectional RPC")
        rpc_call = int(input("Which rpc would you like: "))
        
        if rpc_call == 1:
            hello_request = greet_pb2.HelloRequest(name="athul", greeting="hello")
            hello_reply = stub.SayHello(hello_request)
            print("Reply from server: ", hello_reply)
        
        if rpc_call == 2:
            hello_request = greet_pb2.HelloRequest(name="athul", greeting="hello")
            hello_replies = stub.ParrotSaysHello(hello_request)
            for hello_reply in hello_replies:
                print("Reply from server: ", hello_reply)
                
        if rpc_call == 3:
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())
            print("Reply from server: ", delayed_reply)
        
        if rpc_call == 4:
            responses = stub.InteractingHello(get_client_stream_requests())
            for response in responses:
                print("Reply from server: ", response)
            

if __name__ == '__main__':
    run()