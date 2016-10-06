# TodoMVC test coding exercise

Run 'pip install -U selenium' to get latest selenium, and 'py testTody.py' to run the tests.

I'd never used a web test framework before so I read a bit about Selenium and started coding. My biggest difficulty was the inbuilt webdriver in Firefox was broken in a recent release, and as I'm new to Selenium I spent a bit of time trying to figure out what was wrong. On Stackoverflow the consensus seems to be to roll back to an earlier version of Firefox or work around the changes, so I switched to using the Chrome webdriver and I got it working (I rolled back to Firefox 45.4 esr and it works too).

The commented out code is what I originally wrote and executes all the tests sequentially, but this morning I changed it to how it is now; using unittest which means you can easily see which tests pass or fail, and each are independent so they can be run in parallel.

I've tested the tests on Windows using Chrome and Firefox 45.4. By default it's using Chrome, to use another browser change line 15 and you might also need to put the webdriver for your os and browser in the directory. Firefox <= 46 will probably work without the webdriver.