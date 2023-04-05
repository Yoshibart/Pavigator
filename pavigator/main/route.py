import heapq

def RouteMST(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    prev_nodes = {}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # Stop once we reach the destination node
        if current_node == end:
            break

        # Goto start of whileloop if we've already found a shorter path
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Update distance and add to priority queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                prev_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct shortest path
    path = []
    current_node = end
    while current_node != start:
        path.insert(0, current_node)
        current_node = prev_nodes[current_node]
    path.insert(0, start)

    return path
