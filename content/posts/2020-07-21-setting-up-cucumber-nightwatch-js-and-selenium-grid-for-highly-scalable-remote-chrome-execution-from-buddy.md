---
title: Setting up Cucumber, Nightwatch.js and Selenium Grid for highly scalable remote Chrome execution from Buddy
slug: setting-up-cucumber-nightwatch-js-and-selenium-grid-for-highly-scalable-remote-chrome-execution-from-buddy
date: 2020-07-21T11:26:00.000Z
type: "post"
---



## Technical Overview

- [Nightwatch.js](https://nightwatchjs.org/) - [Node.js](https://nodejs.org/en/) powered end-to-end testing framework
- [Cucumber](https://cucumber.io/) - BDD testing framework that sits on top of Nightwatch.js
- [Selenium Grid](https://www.selenium.dev/) - Highly scalable browser automation for running tests
- [Buddy](https://buddy.works/) - CI/CD pipeline

## End Goal

The outcome of setting up this pipeline will allow us to execute end-to-end tests from anywhere, in any development environment.

Having Selenium Grid as a public endpoint also allows us to execute these end-to-end tests from our existing CI/CD pipeline.

## Selenium Grid

Selenium Grid, in short, is a central server that our test framework (Nightwatch.js) will be able to send requests to. Selenium Grid can spin up multiple Nodes which will allow for test execution against remote-controlled headless Chrome Instances.

The beauty of Selenium Grid is that it is highly scalable. Each Node can have a defined amount of Chrome instances (or Firefox, Internet Explorer, and Opera). And a grid can register an infinite amount of Nodes.

Nodes can either live on the same instance as the Selenium Grid Hub (the central processing endpoint), or the Nodes can live on separate server instances to allow for fine-tuned server scaling for each node.

## Nightwatch.js

We wanted to integrate Nightwatch.js into our end-to-end testing pipelines because it integrates with our existing microservices flawlessly.

Tests are simple to write, with the comprehensive API developer documentation. And is fully supported by the community if we run into anything tricky.

## Cucumber

Cucumber allows us to write tests in a human-readable, user story kind of manner. This works great for our inhouse testers as it can be tricky for them to write tests from a technical mindset. Having the tests as user stories already integrate with our current working methods. This also helps us as a team to think about test scenarios from the perspective of a user.

Here's an example of a Cucumber test:

    Feature: Google
    
        Scenario: Google webpage loads
    
            Given I navigate to Google
            And I log in with a valid-user
            And I use the search filter to search for "Test Automation"
            Then the title is "Google - Test Automation"
    

Cucumber will 'translate' this into a full test and pass it over to Nightwatch, which will execute the tests.

# Putting it all together

## Setting up Cucumber to use Nightwatch.js

This was tricky at first as Nightwatch.js is a standalone test runner, it works without Cucumber. Tests can be written by only using Nightwatch.js if BDD isn't needed. But we required Cucumber as we wanted to involve our testers as much as possible.

### Installing the necessary npm packages

To be able to run Cucumber with Nightwatch.js, we need some packages from [npm](https://www.npmjs.com/).

We'll need the following:

- cucumber
- cucumber-pretty
- nightwatch
- nightwatch-api

These can be installed by running the following command (global install)

    sudo npm i -g cucumber cucumber-pretty nightwatch nightwatch-api
    

### Setting up your node environment to execute end-to-end tests

Next, we need to add a build script to our `package.json` to allow us to run Cucumber from npm

    // package.json
    "scripts": {
            ...
            "e2e-test": "cucumber-js --require cucumber.conf.js --require tests/**/step-definitions --format node_modules/cucumber-pretty tests/*"
        },
    

We also need to create a `cucumber.conf.js` file to specify our Cucumber settings.

    // cucumber.conf.js
    const { setDefaultTimeout, AfterAll, BeforeAll } = require('cucumber');
    const { createSession, closeSession } = require('nightwatch-api');
    
    setDefaultTimeout(60000);
    
    BeforeAll(async () => {
      await createSession();
    });
    
    AfterAll(async () => {
      await closeSession();
    });
    

Finally, we need to create a `nightwatch.conf.js` file to add our execution settings

    // nightwatch.conf.js
    module.exports = {
        "src_folders" : ["tests/"],
    
        "selenium" : {
            "start_process" : false, // Important for running test execution on a remote Selenium Grid
            "host" : "seleniumgrid.example.com", // Endpoint for Selenium Grid
            "port" : 443,
            "use_ssl": true
        },
    
        "test_settings" : {
            "default" : {
                "selenium_port": 443,
                "selenium_host": "seleniumgrid.example.com", // Endpoint for Selenium Grid
                "use_ssl": true,
                "desiredCapabilities": {
                    "browserName": "chrome", // Specified Browser
                    "javascriptEnabled": true,
                    "acceptSslCerts": true,
                    "chromeOptions": {
                        "w3c": false, // Important
                        "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu", "--disable-dev-shm-usage"], // Important
                    },
                    // This is to pass config when using Nodes
                    "goog:chromeOptions": {
                        "w3c": false, // Important
                        "args": ["--headless", "--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu", "--disable-dev-shm-usage"], // Important
                    }
                    // Both chromeOptions objects are required for this to work
                },
            },
        }
    }
    

That's all the configuration needed, your folder structure should now look like this:

    project_root/
      package.json
      cucumber.conf.js
      nightwatch.conf.js
    

### Folder Structure

Cucumber is very particular about folder structure. The recommended folder structure is the following:

    project_root
    ├ cucumber.conf.js
    ├ nightwatch.conf.js
    ├ package.json
    └ tests
        └ features
            ├ ebay.feature
            ├ google.feature
            └ step-definitions
                ├ ebay.js
                ├ google.js
                └ shared.js
    

## Provisioning Selenium Grid

This is where we create the Selenium Grid server. We host ours in AWS EC2 on a T2.micro Ubuntu Server instance. We tested with CentOS but could not get everything working properly. Ubuntu Server works flawlessly and is highly recommended if you're looking at setting this up.

Here is a script that I wrote to provision Selenium Grid on Ubuntu Server. It can copy this script and save it as a `.sh` file. Then execute this file in the scope of your Linux instance. It will require some tweaking of the paths to match up with your server.

    #! /bin/bash
    
    # This script requires default-jre and unzip to be installed
    # Run the following as Sudo
    # `sudo apt-get update && sudo apt-get install -y default-jre unzip xvfb screen`
    
    # Enable execute permissions with
    # `sudo chmod +x setup.sh`
    
    # Please execute this script as your user
    # e.g `sudo -u your_user ./setup.sh`
    
    cd $HOME
    
    mkdir TestAutomation
    cd TestAutomation
    
    # Download Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    
    # Install Chrome
    sudo apt install -y ./google-chrome-stable_current_amd64.deb
    
    # Remove deb file
    rm google-chrome-stable_current_amd64.deb
    
    # Download Selenium Grid
    wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar
    
    # Download Chrome Driver
    wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
    
    unzip chromedriver_linux64.zip
    
    rm chromedriver_linux64.zip
    
    # Create spawn files
    export DISPLAY=:0.0
    echo "screen -d -m java -jar /home/ubuntu/TestAutomation/selenium-server-standalone-3.141.59.jar -role hub" > ../spawn-hub.sh
    echo "screen -d -m xvfb-run --auto-servernum --server-num=0 java -Dwebdriver.chrome.driver=/home/ubuntu/TestAutomation/chromedriver -Dwebdriver.chrome.bin=/usr/bin/google-chrome -jar /home/ubuntu/TestAutomation/selenium-server-standalone-3.141.59.jar -role node -hub http://localhost:4444/grid/register -browser browserName=chrome,maxInstances=10" > ../spawn-node.sh
    
    # Set spawn file permissions
    chmod +x ../spawn-*
    

Executing the generated `spawn-hub.sh` will result in Selenium Grid spinning up on the port `4444`. The grid will then listen for Nodes.

To spin up a Node, execute the generated script `spawn-node.sh`. This command can be executed multiple times to spin up multiple Nodes.

TIP: If you want your Nodes on separate instances, copy the above provisioning script and execute it on your Node instances. But only execute the `spawn-node.sh` script.

## Tying it together

Now all that is needed is to expose your Selenium Grid server to the web. I won't go into detail on how to do this, as it's different for everyone.

Make sure that you update your `nightwatch.conf.js` file to point to your new hosted endpoint.

## Executing the tests

All that is now needed to run these tests is the following command:

    npm run e2e-test
    

To recap...

1. This will run the Cucumber command to find all cucumber tests and their respective step-definitions.
2. Pass them to Nightwatch to act as the test handler.
3. Nightwatch will pass those tests to our remote Selenium Grid instance.
4. Selenium Grid will distribute the tests to the test Nodes.
5. The test Nodes will spin up Google Chrome and execute their assigned tests.
6. Once finished, passing back the test output to Nightwatch.js and displaying the output in the npm console.

## Chrome Plugins

It's also worth mentioning that this execution pipeline allows for a full instance of Google Chrome to run, which means that you can use browser plugins as part of your execution pipeline. This is a rare thing to achieve but is possible using the above steps.

## Adding all this to Buddy

Adding to Buddy was relatively simple. We created a small pipeline to pull down the latest change from this test repository.

Buddy allows an action to call another pipeline. So as part of our microservice pipeline, we call the external tests pipeline to execute the tests.

    - action: "Run Selenium Grid Tests"
        type: "RUN_NEXT_PIPELINE"
        wait: true
        comment: "Triggered by $BUDDY_PIPELINE_NAME execution #$BUDDY_EXECUTION_ID"
        trigger_condition: "ALWAYS"
        revision: "HEAD"
        variables:
        - key: "TEST_TAGS"
          value: "\"@google\""
        next_project_name: "automationtests"
        next_pipeline_name: "Run Selenium Grid Tests"
    

We used Tags to be able to execute specific tests as part of our deployment, that's the `TEST_TAGS` variable you can see in the above snippet.

Here's our pipeline for running the test project:

    - pipeline: "Run Selenium Grid Tests"
      trigger_mode: "MANUAL"
      ref_name: "master"
      ref_type: "BRANCH"
      trigger_condition: "ALWAYS"
      actions:
      - action: "Format Test Tags"
        type: "BUILD"
        working_directory: "/buddy/automationtests"
        docker_image_name: "library/ubuntu"
        docker_image_tag: "18.04"
        execute_commands:
        - "TAGS=$TEST_TAGS"
        - "NODE_ENV=$ENV"
        volume_mappings:
        - "/:/buddy/automationtests"
        trigger_condition: "ALWAYS"
        shell: "BASH"
      - action: "Find & replace"
        type: "REPLACE"
        local_path: "package.json"
        replacements:
        - replace_from: "{TAGS}"
          replace_to: "$TAGS"
        trigger_condition: "ALWAYS"
      - action: "Run tests with Selenium Grid"
        type: "BUILD"
        working_directory: "/buddy/automationtests"
        docker_image_name: "library/node"
        docker_image_tag: "12"
        execute_commands:
        - "# yarn install"
        - "npm install"
        - ""
        - "npm run e2e-test-buddy --silent -- tests/* >> test-output.txt"
        volume_mappings:
        - "/:/buddy/automationtests"
        trigger_condition: "ALWAYS"
        shell: "BASH"
        execute_every_command: true
      variables:
      - key: "NODE_ENV"
        settable: true
    

## That's it

All done, you should now have remote test execution.

Please get in touch with us if you have any issues

Thanks for reading.
