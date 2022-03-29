# LinkedIn Profile Scraper
LinkedIn profile scraper is developed using Selenium and Beautifull soup libraries in python. It can scrap data from public Linedin User profiles. 


This scraper will extract publicly available data: 

**🧑‍🎨 Profile:** name, location

**👨‍💼 Experiences:** job title, most recent company,company url



## Getting started
In order to scrape LinkedIn profiles, you need to make sure the scraper is logged-in into LinkedIn. For that you need to enter your Linkedin account email and Password in Config file. I suggest you enable all the privacy options so people don't see you visiting their profiles when using the scraper.
You will have to provide link to the profile which you want to scrap.

# How to Run 

- Clone the repository
- Setup Virtual environment
```
$ python3 -m venv env
```
- Activate the virtual environment
```
$ source env/Source/activate
```
- Install dependencies using
```
$ pip install -r requirements.txt
```
-  Enter your email and Password in config file and run the scraper with links to profiles to scrap

### About the performance
- Upon start the module will open a headless browser session using Chromium.
- Scraping usually takes a few seconds, because the script needs to scroll through the page and expand several elements in order for all the data to appear.

### Usage limits
LinkedIn has some usage limits in place. Please respect those and use their options to increase limits. More info: [LinkedIn Commercial Use Limit](https://www.linkedin.com/help/linkedin/answer/52950)

## Reference

https://github.com/SuwaidAslam/LinkedIn-profile-scraper
