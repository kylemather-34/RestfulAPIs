"""
Write an HTTP server that will accept requests to start a virtual machine (VM) and to
shut it down.

Start:

    POST http://localhost:8000/vm/start

    {
        "cpu_count": 2,
        "mem_size_gb": 32,
        "image": "ubuntu-22.04"
    }

Validate that:
    - cpu_count is bigger than 0 and less than 65
    - mem_size_gb is bigger than 8 and smaller than 1025
    - image is one of "ubuntu-24.04", "debian:bookworm" or "alpine:3.20"

Return a JSON message with new VM id:
    {
        "id": "c9abe3b66fc544c78e355968119081ed"
    }

Stop:

    POST http://localhost:8000/vm/{id}/stop

Validate that {id} is a valid VM id and return a JSON message:
    {
        "id": "c9abe3b66fc544c78e355968119081ed",
        "spec": {
            "cpu_count": 2,
            "mem_size_gb": 32,
            "image": "ubuntu-22.04"
        }
    }
"""
