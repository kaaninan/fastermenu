# Pages

| Link | Description |
|--|--|
|/redirect  | QR Code Redirect |
|/order  | Enterprise Menu Page |
|/cart  | Shopping Cart API |
|/enterprise  | Enterprise Admin |
|/admin  | Django Admin (for system admin) |
|/health  | Health Check for AWS Elastic Beanstalk |

# Current System

**Domain & HostedZone:** AWS Route 53

**Static**
1. **Introduction:** fastermenu.com -> AWS CloudFront + S3 with SSL

**Application**
1. **Production:** app.fastermenu.com
2. **Staging:** beta.fastermenu.com

 **app.fastermenu.com**
**Source:** AWS Elastic Beanstalk - fastermenu-production
**Load Balancer:** AWS Application Load Balancer with SSL
**Database:** AWS RDS PostgreSQL - fastermenu-db-production
**Pipeline:** CodePipeline - Connected GitHub master branch

**beta.fastermenu.com**
**Source:** DigitalOcean Droplet
**Database:** AWS RDS PostgreSQL - fastermenu-db-production
**Deployment:** Fabfile

## Deploy AWS Elastic Beanstalk
Elastic Beanstalk configuration files in: **.ebextensions/**

**For production with manual deployment:**

	git clone git@github.com:kaaninan/fastermenu.git
	cd fastermenu
	virtualenv .venv -p python3
	source .venv/bin/activate
	pip install -r requirements.txt
	git add -A
	git commit -am 'deployment'
	eb init
	eb deploy

**For production with pipeline:**

	git clone git@github.com:kaaninan/fastermenu.git
	cd fastermenu
	virtualenv .venv -p python3
	source .venv/bin/activate
	pip install -r requirements.txt
	git add -A
	git commit -am 'deployment'
	git push origin master

## Deploy DigitalOcean
Server configuration files in: **fabfile.py**

**Deploy App:**

	git add -A
	git commit -am 'deployment'
	git push origin beta
	fab deploy

**Setup New Server:**

	git clone git@github.com:kaaninan/fastermenu.git
	cd fastermenu
	virtualenv .venv -p python3
	source .venv/bin/activate
	pip install -r requirements.txt
	git add -A
	git commit -am 'deployment'
	git push origin beta
	fab bootstrap

