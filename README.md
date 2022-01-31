# opcua_client

Repsoitory für das iAT Projekt im WS21/22

## How to run

### Windows with virtual environment

#### 0. Install dependencies

1. Download Kinect for Windows Runtime 2.2.1811 (https://www.microsoft.com/en-us/download/details.aspx?id=57578)
2. Install vcredist_x64.exe
3. Install kinectsensor.inf
4. Install KinectRuntime-x64.msi
5. Download Kinect for Windows SDK 2.0 (https://www.microsoft.com/en-us/download/details.aspx?id=44561)
6. Install KinectSDK-v2.0_1409-Setup.exe
7. pip install -r requirements.txt

#### 1. Run the mock server (only necessary when official server is not available)

1.1 Activate the virtual environment
```cmd
.\venv\Scripts\activate
```

1.2 Navigate into server folder
```cmd
cd .\server\
```

1.3 Run server.py with python
```cmd
python .\server.py
```

#### 2. Run the client
2.1 Set `kinect_connected` in `main.py` to `True` if you want to run the client with the kinect
or to `False` if you just want to try the client-server interaction and the frontend.

2.2 Set `self.simulation` in `main.py` to `True` if you want to use the mock server instead 
of the official IfA "Kleinversuchsanlage" Server or to `False` otherwise.

2.3 Run main.py with python
```cmd
python .\main.py
```

