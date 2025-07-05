import httpx

BASE_URL = "http://20.175.245.192"

def test_map():
    print("Testing /map endpoints...")
    #get map
    response = httpx.get(f"{BASE_URL}/map")
    print("GET /map:", response.json())
    #update map
    response = httpx.put(f"{BASE_URL}/map", params={"height": 4, "width": 4})
    print("PUT /map:", response.json())
    #get map again to ensure that the map has been updated
    response = httpx.get(f"{BASE_URL}/map")
    print("GET /map:", response.json())


def test_mines():
    print("\nTesting /mines endpoints...")
    # Get all mines
    response = httpx.get(f"{BASE_URL}/mines")
    print("GET /mines:", response.json())
    # Get a single mine
    response = httpx.get(f"{BASE_URL}/mines/{1}")
    print(f"GET /mines/{1}:", response.json())
    # Delete the mine
    response = httpx.delete(f"{BASE_URL}/mines/{1}")
    print(f"DELETE /mines/{1}:", response.json())
    # Get all mines to show that the chosen mine have been deleted
    response = httpx.get(f"{BASE_URL}/mines")
    print("GET /mines:", response.json())
    # Create a mine
    response = httpx.post(f"{BASE_URL}/mines", params={"serial_number": "M123", "x": 0, "y": 3})
    print("POST /mines:", response.json())
    # Get all mines to see if the mine have been created
    response = httpx.get(f"{BASE_URL}/mines")
    print("GET /mines:", response.json())
    # also check the map to ensure it has been updated
    response = httpx.get(f"{BASE_URL}/map")
    print("GET /map:", response.json())
    # Update the mine
    response = httpx.put(f"{BASE_URL}/mines/{3}", params={"x": 0, "y": 0})
    print(f"PUT /mines/{3}:", response.json())
    # Get all mines to see if the mine have been updated
    response = httpx.get(f"{BASE_URL}/mines")
    print("GET /mines:", response.json())
    #also check the map to ensure it has been updated
    response = httpx.get(f"{BASE_URL}/map")
    print("GET /map:", response.json())

def test_rovers():
    print("\nTesting /rovers endpoints...")
    # Get all rovers
    response = httpx.get(f"{BASE_URL}/rovers")
    print("GET /rovers:", response.json())
    # Get a single rover
    response = httpx.get(f"{BASE_URL}/rovers/{1}")
    print(f"GET /rovers/{1}:", response.json())
    # Create a rover
    response = httpx.post(f"{BASE_URL}/rovers", params={"commands": "LLLRRRMMMMMMMMMMRMRMRMLDDMMM"})
    print("POST /rovers:", response.json())
    # # Get all rovers
    response = httpx.get(f"{BASE_URL}/rovers")
    print("GET /rovers:", response.json())
    # Update the rover's commands
    response = httpx.put(f"{BASE_URL}/rovers/{2}", params={"commands": "MMMMMMMMM"})
    print(f"PUT /rovers/{2}:", response.json())
    # Get all rovers
    response = httpx.get(f"{BASE_URL}/rovers")
    print("GET /rovers:", response.json())
    # Delete the rover
    response = httpx.delete(f"{BASE_URL}/rovers/{2}")
    print(f"DELETE /rovers/{2}:", response.json())
    # Get all rovers
    response = httpx.get(f"{BASE_URL}/rovers")
    print("GET /rovers:", response.json())
    # Dispatch the rover
    response = httpx.post(f"{BASE_URL}/rovers/{10}/dispatch",timeout=300)
    print(f"POST /rovers/{10}/dispatch:", response.json())
    response = httpx.get(f"{BASE_URL}/map")
    print("GET /map:", response.json())


if __name__ == "__main__":
    # test_map()
    # test_mines()
    # test_rovers()
    # Get all mines
    response = httpx.get(f"{BASE_URL}/mines")
    print("GET /mines:", response.json())

