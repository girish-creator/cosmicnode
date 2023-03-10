# CosmicNode
A test automation repository in GitHub for CosmicNode.


## GitHub
#### Install Git on your machine
- https://git-scm.com/download/win

#### You can also try to install GitHub application
- https://desktop.github.com/

#### Follow the below link for setting up SSH keys to access GitHub
-  https://docs.github.com/en/authentication/connecting-to-github-with-ssh\

#### Clone the CosmicNode devops project from GitHub:
-  git@github.com:cosmicnodenl/devops-automation.git

#### Checkout the develop branch
-  cd /devops-automation
-  git checkout develop


## Python
-  Install the latest python version from the python.org which should by default come with pip.
-      https://www.python.org/downloads/

## Docker
#### Follow the docker documentation for installing and configuring Docker on your machine
-  https://docs.docker.com/get-docker/

## OpenVPN
##### VPN is only needed when you are not connected directly to the CosmicNode network
#### Windows
-  https://openvpn.net/client-connect-vpn-for-windows/

#### Linux
-  https://openvpn.net/vpn-server-resources/connecting-to-access-server-with-linux/

#### For connecting to the CosmicNode OpenVPN, import the config file which you can get from the OpenVPN network owner

## Jenkins
#### If you want to add your current system as an agent/machine to run tests for CosmicNode.
-  Connect to the OpenVPN of CosmicNode / on the CosmicNode network directly.
-  Open the Jenkins server link:
-      http://100.96.1.50:8080/
-  Got to 'Manage Jenkins' -> 'Manage nodes and clouds' -> 'New Node'
-  Provide a unique functional/related name for your agent machine.
-  Select the type of agent you want to create
-     'Permanant' - as the name suggests
-     'Copy from Existing' - provide a name of an existing agent and all the configurations from that agent will be copied for your agent.
-  Jenkins will provide an agent.jar file which can be directly downloaded
-  It will also show the exact java run command to add your system as a jenkins agent.
-  Example java command:
-     Run from agent command line:
      java -jar agent.jar -jnlpUrl http://100.96.1.50:8080/computer/Jenkins%2DWindows%2DWith%2DDocker/jenkins-agent.jnlp -secret keyword -workDir "C:\Jenkins"
-     Run from agent command line, with the secret stored in a file:
      echo keyword > secret-file
      java -jar agent.jar -jnlpUrl http://100.96.1.50:8080/computer/Jenkins%2DWindows%2DWith%2DDocker/jenkins-agent.jnlp -secret @secret-file -workDir "C:\Jenkins"

#### Run a Jenkins job
-  Run all the CosmicNode API tests by going to the below link:
-     http://100.96.1.50:8080/job/cosmicnode-api-tester/
-  select 'Build Now' option for the current job and if the required agents are available to run the job, the job will start running.
-  the job will generate logs for each run which you can view my visiting the console output page from the latest run.


## Build a test case using Builder
-  Once, you have the code from GitHub
-  Create a local python virtual environment, using virtualenv
-      pip install virtualenv
-      virtualenv venv # This will use the base python interpretor on your system and create a virtual python environment in the current folder
-  Activate the newly created virtual environment
-      Windows
          cd venv/Scripts
          ./activate
-      Linux
          cd venv/bin
          source activate
-  Similarly, if you want to deactivate the virtual environment
-      Windows
          cd venv/Scripts
          ./deactivate
-      Linux
          cd venv/bin
          source deactivate
-  Install all the requirements for the current project, from the root folder of the project run the below command:
-      pip install requirements.txt

-  In the main function add the required arguments for adding a new test case.
-     
      if __name__ == "__main__": 
        args_api = {'api_list': [{"api_endpoint": "http://192.168.1.27/rpc/Command.PWM",
                          "operation": "POST",
                          "payload": "{\"cmd\":210,\"address\":65535,\"params\":[50]}",
                          "headers": "{'Content-Type': 'application/json'}",
                          'api_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                                                 "expected_value": 200}
                                                ]
                          }]
                }
        test_builder_obj = TestBuilder(test_name='test_new_api', argument_dict=args_api_serial)
        test_builder_obj.run()
-  Make changes to the arguments and provide a new test case name if you want to create a new test case
-      (Note: if you do not update the test case name, then the older test case with the same would be updated with the new arguments.)