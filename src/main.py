
from detector import HybridFakeNewsDetector

def main():
    print("\n=== HYBRID FAKE NEWS DETECTOR ===\n")

    # -----------------------------------------
    # ADD YOUR API KEYS HERE
    # -----------------------------------------
    api_keys = {
        "gnews": "add-gnews-apikey",
        "newsapi": "add-newsapi-apikey",
        # "bing": "YOUR_BING_KEY_HERE"   # Optional
    }

    # Initialize detector with API keys
    detector = HybridFakeNewsDetector(api_keys=api_keys)

    # Command-line loop
    while True:
        claim = input("\nEnter a claim to verify (or 'exit'): ")

        if claim.lower().strip() == "exit":
            print("\nExiting system. Goodbye!\n")
            break

        result = detector.detect(claim)
        detector.display(result)

if __name__ == "__main__":
    main()

