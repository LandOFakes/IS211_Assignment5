import csv
from collections import deque
import sys

class Request:
    def __init__(self, time, filename, duration):
        self.time = int(time) 
        self.filename = filename  
        self.duration = int(duration) 

class Server:
    def __init__(self):
        self.queue = deque()  
        self.current_time = 0  

    def process_request(self, request):
        
        self.queue.append(request)
    
    def serve(self):
        if self.queue:
           
            request = self.queue.popleft()
            wait_time = max(0, self.current_time - request.time)
            self.current_time = max(self.current_time, request.time) + request.duration
            return wait_time
        return 0

def simulateOneServer(filename):
    requests = []
    
    
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            requests.append(Request(*row))
    
    # Create a single server
    server = Server()
    total_wait_time = 0
    total_requests = len(requests)
    
    # Process each request
    for request in requests:
        server.process_request(request)
        wait_time = server.serve()
        total_wait_time += wait_time
    
    # Calculate the average wait time
    average_wait_time = total_wait_time / total_requests if total_requests > 0 else 0
    return average_wait_time

def simulateManyServers(filename, num_servers):
    requests = []
    
    # Read the CSV file and create Request objects
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            requests.append(Request(*row))
    
    # Create multiple servers
    servers = [Server() for _ in range(num_servers)]
    total_wait_time = 0
    total_requests = len(requests)
    
    # Distribute requests across servers in a round-robin fashion
    for i, request in enumerate(requests):
        server = servers[i % num_servers]  # Round-robin distribution
        server.process_request(request)
    
    # Process each request and calculate wait time
    for server in servers:
        while server.queue:
            wait_time = server.serve()
            total_wait_time += wait_time
    
    # Calculate the average wait time
    average_wait_time = total_wait_time / total_requests if total_requests > 0 else 0
    return average_wait_time

def main():
   
    filename = input("Enter the filename (CSV): ")
    num_servers_str = input("Enter the number of servers (default is 1): ")
    
    
    try:
        num_servers = int(num_servers_str)
    except ValueError:
        print("Invalid input for number of servers. Using default value of 1.")
        num_servers = 1 
    
    if num_servers == 1:
        avg_wait_time = simulateOneServer(filename)
    else:
        avg_wait_time = simulateManyServers(filename, num_servers)
    
    print(f"Average wait time: {avg_wait_time:.2f} seconds")

if __name__ == "__main__":
    main()
