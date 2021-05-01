.PHONY: all package blr mum 
.DEFAULT_GOAL := all

all: blr mum

package:
	@pip3 install --target ./package -r requirements.txt
	@cd package && zip -r9 ../function.zip .
	@zip -q -g function.zip lambda_function.py slots.py publish_to_discord.py

blr: package
	AWS_REGION=ap-south-1 aws lambda update-function-code --function-name slots-blr --zip-file fileb://function.zip

mum: package
	CITY=mum AWS_REGION=ap-south-1 aws lambda update-function-code --function-name slots-mum --zip-file fileb://function.zip