# Keyboard Event Monitor

## Overview
This project implements a Python-based keyboard event monitoring system with network capabilities. It's designed for legitimate system monitoring and diagnostic purposes, featuring efficient event processing and network transmission.

## Technical Features
- Asynchronous keyboard event processing
- Memory-efficient buffering system
- Network transmission with retry capability
- Thread-safe operations
- Configurable monitoring intervals

## Requirements
- Python 3.7+
- Required packages:
  ```
  pynput>=1.7.3
  ```

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit the `key.py` file to set the following parameters:
```python
SERVER_IP_ADDR = "your_server_ip"
SERVER_PORT = your_port_number
TIME_INTERVAL = transmission_interval_in_seconds
```

## Project Structure
```
.
├── client.py        # Main implementation file
├── key.py          # Configuration constants
└── README.md       # This file
```

## Implementation Details

### Core Components

#### KeyLogger Class
The main class handling keyboard monitoring and event processing.

Key features:
- Event buffering using StringIO
- Thread-safe operations with buffer locks
- Queued event processing
- Configurable network transmission

#### Network Operations
- TCP-based transmission
- Automatic retry on connection failure
- Server acknowledgment handling

#### Performance Optimizations
- Asynchronous event processing
- Memory-efficient buffering
- Reduced disk I/O
- Optimized thread management

## Usage
Run the program with:
```bash
python client.py
```

The program will:
1. Initialize the monitoring system
2. Create necessary directories
3. Begin processing keyboard events
4. Transmit data at configured intervals

## Error Handling
The system includes comprehensive error handling for:
- Network connectivity issues
- File system operations
- Memory management
- Thread synchronization

## Monitoring and Logging
- Console output for diagnostic information
- Error logging for troubleshooting
- Network transmission status updates

## Technical Considerations
- CPU usage is optimized through event queuing
- Memory usage is controlled via buffer management
- Network transmission is handled in separate threads
- File I/O is minimized to improve performance

## Development and Testing
For development purposes:
1. Set shorter `TIME_INTERVAL` values
2. Monitor console output for diagnostics
3. Check network connectivity with test server

## Performance
The system is optimized for minimal system impact:
- Efficient event queuing
- Controlled memory usage
- Reduced disk operations
- Optimized thread management

## Troubleshooting
Common issues and solutions:
1. Connection failures:
   - Verify server address and port
   - Check network connectivity
   - Confirm firewall settings

2. Performance issues:
   - Adjust queue size
   - Modify processing intervals
   - Check system resources

