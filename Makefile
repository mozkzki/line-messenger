.PHONY: test start

test:
	npm run test

start:
	aws lambda invoke --no-cli-auto-prompt --function-name dev-line-messenger response.json --log-type Tail --query 'LogResult' --output text | base64 -d
