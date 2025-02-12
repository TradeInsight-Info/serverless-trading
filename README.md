# Serverless Trading

This is a project to use Alpaca-Py SDK and AWS Lambda to create a serverless trading bot.

- [jupyter notebook](https://github.com/TradeInsight-Info/serverless-trading/blob/master/playground.ipynb)
- [medium - Serverless Trading - Run Trading Algorithm on AWS Lambda](https://medium.com/@TechTim42/serverless-trading-run-trading-algorithm-on-aws-lambda-5f04bc9b42bb)



## Environment Variables
- `ALPACA_KEY`
- `ALPACA_SECRET`


- update environment variables on AWS Lambda

```bash
aws lambda update-function-configuration \
--function-name {function_arn} \
--environment "Variables={ALPACA_KEY=a,ALPACA_SECRET=b}"
```
