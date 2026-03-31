import google.generativeai as genai

try:
    # __version__ attribute exists in newer versions
    print(f"Installed google-generativeai version: {genai.__version__}")
    print("\nSUCCESS: A modern version of the library is installed.")
except AttributeError:
    print("\nERROR: An old, incompatible version of the library is installed.")
    print("Please run 'pip install --upgrade google-generativeai' again.")