from flask import render_template, url_for, request, flash
from mfgdcc import app, coins_df, coins_df_names, coins_df_statuses


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        coin_name = request.form['coin']
        status = request.form['status']

        if coin_name == 'all' and status == 'all':
            return render_template('tabular.html', header_caption='Tabular View', coins_df_names=coins_df_names,
                                   coins_df_statuses=coins_df_statuses, coins_df=coins_df)
        elif coin_name == 'all':
            coins_df_filtered = coins_df[coins_df['Status'] == status]
            return render_template('tabular_filtered.html', header_caption='Tabular View (Filtered)',
                                   coins_df=coins_df_filtered)
        elif status == 'all':
            coins_df_filtered = coins_df[coins_df['Name'] == coin_name]
            return render_template('tabular_filtered.html', header_caption='Tabular View (Filtered)',
                                   coins_df=coins_df_filtered)
        else:
            coins_df_filtered = coins_df[coins_df['Name'] == coin_name]
            coins_df_filtered = coins_df_filtered[coins_df_filtered['Status'] == status]
            return render_template('tabular_filtered.html', header_caption='Tabular View (Filtered)',
                                   coins_df=coins_df_filtered)

    return render_template('tabular.html', header_caption='Tabular View', coins_df_names=coins_df_names,
                           coins_df_statuses=coins_df_statuses, coins_df=coins_df)


@app.route('/charts/marketcap', methods=['GET', 'POST'])
def charts_marketcap():
    return chart_request('Market Cap', 'bar', 'charts_marketcap')


@app.route('/charts/price', methods=['GET', 'POST'])
def charts_price():
    return chart_request('Price', 'line', 'charts_price')


@app.route('/charts/supply', methods=['GET', 'POST'])
def charts_supply():
    return chart_request('Supply', 'bar', 'charts_supply')


def chart_request(chart_data_type, chart_type, form_url):

    header_caption = chart_data_type + ' Charting'

    if request.method == "POST":

        valid_request = True
        coins = request.form.getlist('coins')
        if not coins:
            flash("Please select at least one coin.")
            valid_request = False
        try:
            status = request.form['status']
        except KeyError:
            flash("Please choose a status filter.")
            valid_request = False

        if valid_request:

            available_colors = ['#3e95cd', '#8e5ea2', '#3cba9f', '#e8c3b9', '#c45850']
            color_choice = 0
            labels = []
            color_dict = {}
            data_dict = {}
            stacked_bars = False

            for coin_name in coins:
                coins_df_filtered = coins_df[coins_df['Name'] == coin_name]
                if status != 'all':
                    coins_df_filtered = coins_df_filtered[coins_df_filtered['Status'] == status]

                if chart_data_type == 'Price':
                    if len(coins) > 1:
                        if coins_df_filtered['Price'].iloc[0] == 0:
                            err_message = "Cannot normalize the price of " + coin_name +\
                                          " because the data set ends with a 0."
                            flash(err_message)
                            continue
                        data = coins_df_filtered['Price'].div(coins_df_filtered['Price'].iloc[0])
                        data = data.tolist()
                    else:
                        data = coins_df_filtered['Price'].tolist()
                else:
                    data = coins_df_filtered[chart_data_type].tolist()
                    if len(coins) > 1:
                        stacked_bars = True

                data_dict[coin_name] = data
                color_dict[coin_name] = available_colors[color_choice]
                color_choice += 1
                if color_choice == len(available_colors):
                    color_choice = 0

                if len(data) > len(labels):
                    labels = list(range(1, len(data) + 1))

            selected_coins = list(data_dict.keys())

            return render_template('charts.html', selected_coins=selected_coins, selected_status=status,
                                   data=data_dict, labels=labels, colors=color_dict, header_caption=header_caption,
                                   coin_df=coins_df_filtered, coins_df_names=coins_df_names,
                                   coins_df_statuses=coins_df_statuses, chart_type=chart_type,
                                   stacked_bars=stacked_bars, form_url=url_for(form_url))

    return render_template('charts.html', header_caption=header_caption, coins_df_names=coins_df_names,
                           coins_df_statuses=coins_df_statuses, form_url=url_for(form_url))
