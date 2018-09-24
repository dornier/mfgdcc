# Coins.txt Data Parser/Visualizer

By [Brent Dornier](mailto:dornier@gmail.com)

## Getting Started

This application allows the user to load and view a sample data file named coins.txt. It was created using Python 3.7 and the Flask framework. You can get started with it by cloning the github repository:

`git clone https://github.com/dornier/mfgdcc.git`

You can install the necessary packages with the following command:

`pip install -r requirements.txt`

Once these steps are complete, run the application locally by executing:

`python app.py`

Now you should find the app running on the loopback address at port 5000:

[http://localhost:5000](http://localhost:5000)

You can also see the deployed app in action [here](https://dornier.app).

## Discussion

This project makes use of Python, Pandas, Flask, Jinja, HTML, CSS, and JavaScript. I used a responsive HTML5 Boilerplate to generate the HTML and CSS scaffolding. I also made use of [Chart.js](https://www.chartjs.org) for the charting features.

## Requirements

#### "...open, read, and parse the given column separated file..."

The file itself is problematic for a number of reasons:
1. It is not delimited
2. It has missing values
3. There is no apparent scaling

For item 1, I found that using Pandas read_fwf() function along with specified column names was the most effective approach:

`coins_df = pd.read_fwf(os.path.join(base_dir, '..',  'coins.txt'), header=0, names=column_names)`

For item 2, I made the decision to fill missing numerical values with a 0 and non-numerical values with "N/A" in order to make it clear that these values were missing and not interpolated.

For item 3, I made the decision to treat the underlying data as if it were timeseries data, with each entry represnting an equal unit of time. Where some coins may have more entries than others, it is assumed that they begin at a common starting point.

#### "...display the parsed table through a web application..."

The first screen displayed by the app is a tabular view of the entire contents of the file. The user has the ability to filter this table using any non-numberic field (i.e. coin name and status).

#### "Bonus points: also serve Javascript to manipulate (expand, contract, graph, etc) the table in the browser."

From the navigation bar, the user has the ability to choose charts for any of the numeric data (i.e. market cap, price, and supply). When charting market cap or supply, the app will display a bar chart. When charting price data, the app will display a line graph. The user may select a single coin or multiple coins to chart. When selecting multiple coins on the market cap or supply views, the app will display a stacked bar chart. When selecting multiple coins on the price view, the app will normalize the prices and chart their relative performance.

## A Final Note on Testing

There is a unit test framework included in the test folder. It includes tests to verify that all application routes are reachable and responding to well-formed requests. It can be executed using the following command from the root project directory (i.e. the directory containing app.py and coins.txt):

`python -m unittest test.mfgdcc_test`
