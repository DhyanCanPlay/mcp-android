# Model Context Protocol (MCP) Server

A server implementing the Model Context Protocol (MCP) to enable AI agents to intelligently control and interact with Android devices.

## 🚀 About The Project

This project provides a simple Flask-based server that exposes a set of API endpoints to send commands to a connected Android device. The commands are executed using the Android Debug Bridge (ADB).

## 🔧 Getting Started

### Prerequisites

* Python 3.7+
* Pip
* ADB (Android Debug Bridge) installed and in your PATH. You must also have a connected Android device with USB debugging enabled.

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/example/mcp-server.git
   ```
2. Navigate to the project directory:
    ```sh
    cd mcp-server
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Server

To start the server, run the following command:
```sh
python app.py
```
The server will start on `http://127.0.0.1:5000`.

##  API Endpoints

The server exposes the following endpoints:

### `/tap`

* **Method:** `POST`
* **Description:** Taps on the screen at the specified coordinates.
* **Request Body:**
    ```json
    {
        "x": 100,
        "y": 200
    }
    ```

### `/swipe`

* **Method:** `POST`
* **Description:** Swipes from a starting point to an end point.
* **Request Body:**
    ```json
    {
        "x1": 100,
        "y1": 200,
        "x2": 300,
        "y2": 400,
        "duration": 500
    }
    ```

### `/type`

* **Method:** `POST`
* **Description:** Types the given text.
* **Request Body:**
    ```json
    {
        "text": "hello world"
    }
    ```
---
