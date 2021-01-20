# Investing 4.0

Through this app you  will be able to apply some of the basic Value Investing formulas for most of the companies listed on https://www.marketwatch.com/ and https://www.macrotrends.net/ . You can run it on your PC by installing Python 3.8 and the dependencies or simply deploy it as an app on Google App Engine on GCP.

# MarketWatch.com web scrapper
# MacroTrends.com web scrapper
* It ompares 5 different stocks chosen by you, preferably from the same industry

# It Calculates:
* Net Income Growth 5 years 
* Net Income Growth Average
* EPS Growth 5 years 
* EPS Growth Average
* Current Liabilities/Current Cash factor
* Total Liabilities/Total Cash factor
* Price/Earnings
* RORE for last Year
* 5 years RORE Average
* Overpriced

#Demo 
![Demo Image](https://www.skyalleys.com/wp-content/uploads/2021/01/Investing-Stock-Comparision-with-Trend-lines.png)

# Explaining the Overpriced formula:
This formula was developed by myself in order to asses if the current price is corelated with the earnings of the company in the last five years. We know the price 5 years ago, if then the future price after 5 years would have been calculated based on the earnings for the next years, 100% correctly estimated, What price would make sense now?
Components:
* _Price5Years_ - Price 5 years ago
* _Investment_ = _NBShares_ * _Price5Years_
* _RetainedErnings_ = List of Retained earnings for the past 5 years
* _NetPresentValue_ is the NPV of Earnings calculated 5 years ago if all the estimated earnings and the estimating earnings were correct
* _TotalValueYears_ (estimated value gained in the 5 years) = Future Value (-_AverageInflation_, _NbofYears_, 0, -_NetPresentValue_) + * Future Value (-_AverageInflation_, _NbofYears_, 0, -_Investment_)
* _EstimatedPrice_ = _TotalValueYear_s / _NBShares_
* _Overpriced_ = (_PriceNow_ / _EstimatedPrice_) %
