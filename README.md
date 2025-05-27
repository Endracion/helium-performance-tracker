# helium-performance-tracker
Code in Place 2025 final project attempt to write a program that can pull performance data from a live website.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- You have Python 3.x installed.
- You have internet access to download necessary libraries and tools.
- You have Firefox or another Selenium Driver compatible browser (this project uses Firefox).
- This will install the following dependencies: requests, beautifulsoup4, selenium, pandas

## Installation
- Clone the repository
- git clone https://github.com/Endracion/helium-performance-tracker.git
- cd helium-performance-tracker
- Set up a virtual environment (recommended)
  - python -m venv venv
  - source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
- Install dependencies
  - pip install -r requirements.txt
- Install GeckoDriver if using Firefox, else find the appropriate driver.
  - Download GeckoDriver from [here](https://github.com/mozilla/geckodriver/releases) and ensure it's added to your PATH.

## Usage
```python tracker.py```

You will provide a tracker_input.csv where the first column will show the ID of the hotspot you're interested in seeing performance data for.
This ID will be appended to a URL in order to load the page through Selenium. An example file is provided.
In the terminal, you'll be asked for a start and end date.
The program will then loop through all the provided IDs and write the name of the hotspot along with its performance data to a csv that includes the start and end dates.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE V3 - see the LICENSE file for details.