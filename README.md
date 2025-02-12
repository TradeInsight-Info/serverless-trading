# Serverless Trading

This is a project to use Alpaca-Py SDK and AWS Lambda to create a serverless trading bot.

- [jupyter notebook](https://github.com/TradeInsight-Info/serverless-trading/blob/master/playground.ipynb)



## Environment Variables
- `ALPACA_KEY`
- `ALPACA_SECRET`


- update environment variables on AWS Lambda

```bash
aws lambda update-function-configuration \
--function-name {function_arn} \
--environment "Variables={ALPACA_KEY=a,ALPACA_SECRET=b}"
```
