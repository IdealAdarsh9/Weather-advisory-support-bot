from .graph import invoke
import sys
import uuid

if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) or "Is it safe to cycle in Bhopal today?"
    result = invoke(message, str(uuid.uuid4()))
    print(result.get("response", "No response"))
    print("\nTrace:")
    print("\n".join(result.get("trace", [])))
