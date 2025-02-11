# Serverless Trading

This is a project to use Alpaca-Py SDK and AWS Lambda to create a serverless trading bot.



## update environment variables
```bash
aws lambda update-function-configuration \
--function-name arn:aws:lambda:us-east-1:310530271490:function:serverless-trading-TradingFunction-xxx \
--environment "Variables={ALPACA_KEY=a,ALPACA_SECRET=b}"
```