
from detector import HybridFakeNewsDetector

def main():
    print("\n=== HYBRID FAKE NEWS DETECTOR ===\n")

    # -----------------------------------------
    # ADD YOUR API KEYS HERE
    # -----------------------------------------
    api_keys = {
        "gnews": "b70e257b9679d6299b2b169240004cfc",
        "newsapi": "90f06bdf01504ee782f631af24a46b93",
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

