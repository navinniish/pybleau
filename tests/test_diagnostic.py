import inspect
from pybleau.auth import TableauClient

def test_tableau_client_signature():
    """Diagnostic test to see the actual TableauClient constructor signature."""
    signature = inspect.signature(TableauClient.__init__)
    print(f"TableauClient.__init__ signature: {signature}")
    
    # Print parameter names
    params = list(signature.parameters.keys())
    print(f"Parameter names: {params}")
    
    # Try to create with different patterns
    patterns_to_try = [
        # Pattern 1: Positional args
        ("https://test.com", "token", "secret"),
        # Pattern 2: With site
        ("https://test.com", "token", "secret", "site"),
        # Pattern 3: Just server and token  
        ("https://test.com", "token_name_secret_combined"),
    ]
    
    for i, args in enumerate(patterns_to_try):
        try:
            client = TableauClient(*args)
            print(f"Pattern {i+1} WORKED: {args}")
            print(f"Client attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
            break
        except Exception as e:
            print(f"Pattern {i+1} failed: {e}")

if __name__ == "__main__":
    test_tableau_client_signature()
