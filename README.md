
<img width="500" height="500" alt="044016a3-7ad2-498e-80bb-15f5bc65f587" src="https://github.com/user-attachments/assets/3bdf12ee-6a7e-4e00-9a39-0f691345e336" />

# AuthSlicer
AuthSlicer is a Python-based tool designed to assist security testers in analyzing web applications and authentication checks.\n ù
It provides a flexible framework to test multiple header configurations against a target URL and see how the server responds.

# Features
- Send HTTP requests with a variety of custom headers.
- Test multiple common header values in parallel (asynchronous mode).
- Provides status feedback for each request.
- Generates simple proof-of-concept output for each tested header.
- Easy-to-use command-line interface with optional flags for different modes

# Installation
```
git clone https://github.com/yourusername/AuthSlicer.git
cd AuthSlicer
pip install -r requirements.txt
```
# Usage
#### Normal threads, (avoid being detected by WAF)
`python3 AuthSlicer.py -u <target_url>`
#### No WAF? Multi-threads!
`python3 AuthSlicer.py -u <target_url> [--nw]`

# Example
`python3 AuthSlicer.py -u https://example.com --nw`

# Notes
The tool is intended only for authorized security testing. Always have permission before testing a target.
The program supports both synchronous and asynchronous request modes. Asynchronous mode allows sending multiple requests faster. (Usefull if no WAF is set up on the Website)
