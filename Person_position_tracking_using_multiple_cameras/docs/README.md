# Person position tracking using multiple cameras
## Introduction
	The implemention of person tracking system here is based on multiple cameras feed.
	Each camera Instance runs independently and updates detected face in it's feed after every five seconds and updates state(latest detected position) in our database.

### Usage 
#### Steps to Run:
1. clone the Repo:
	```bash
	git clone https://github.com/NikhilKrSharma/video-intelligence.git
	cd Person_position_tracking_using_multiple_cameras
	```
2. Install the requirements:
	```bash
	pip install -r requirements.txt
	```
3. Run Tracker after adding all camera sources(camera/video path) in src/tracker.py
	```bash
	cd src
	python tracker.py
	```

