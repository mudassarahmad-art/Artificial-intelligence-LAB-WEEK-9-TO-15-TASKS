from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# LOAD DATA
model = pickle.load(open('model.pkl', 'rb'))
le = pickle.load(open('le.pkl', 'rb'))
df = pd.read_csv('cleaned_data.csv')


@app.route('/', methods=['GET', 'POST'])
def index():

    avg_price_text = None
    table_html = ""

    if request.method == 'POST':

        budget = float(request.form['budget'])
        ram_val = float(request.form['ram'])
        bat_val = float(request.form['battery'])
        cam_val = float(request.form['camera'])

        # FILTER
        lower_bound = budget * 0.7

        filtered = df[
            (df['Price_num'] <= budget) &
            (df['Price_num'] >= lower_bound)
        ].copy()

        # AI SCORE
        def score(row):
            s = 0
            s += min((row['RAM_num'] / ram_val) * 30, 30)
            s += min((row['Battery_num'] / bat_val) * 25, 25)
            s += min((row['Back_Cam_num'] / cam_val) * 20, 20)

            brand = str(row['Company Name']).lower()
            if 'apple' in brand:
                s += 18
            elif 'samsung' in brand:
                s += 10

            return round(s, 2)

        filtered['AI Score'] = filtered.apply(score, axis=1)

        recs = filtered.sort_values('AI Score', ascending=False).head(6)

        if not recs.empty:

            avg_price = recs['Price_num'].mean()

            avg_price_text = f"""
            <div class="report-grid">

                <div class="report-box">
                    <h3>PKR {avg_price:,.0f}</h3>
                    <p>Average Price</p>
                </div>

                <div class="report-box">
                    <h3>{recs.iloc[0]['Company Name']}</h3>
                    <p>Top Brand</p>
                </div>

                <div class="report-box">
                    <h3>{recs['AI Score'].max()}</h3>
                    <p>Best AI Score</p>
                </div>

                <div class="report-box">
                    <h3>{len(recs)}</h3>
                    <p>Matches Found</p>
                </div>

                <div class="report-box">
                    <h3>{recs.loc[recs['Battery_num'].idxmax()]['Model Name']}</h3>
                    <p>Best Battery</p>
                </div>

                <div class="report-box">
                    <h3>{recs.loc[recs['Back_Cam_num'].idxmax()]['Model Name']}</h3>
                    <p>Best Camera</p>
                </div>

            </div>
            """

            recs['Model Name'] = recs.apply(
                lambda x: f'<a class="search-link" target="_blank" href="https://www.google.com/search?q={x["Company Name"]}+{x["Model Name"]}">{x["Model Name"]}</a>',
                axis=1
            )

            table_html = recs[
                ['Company Name', 'Model Name', 'Launched Price (Pakistan)', 'AI Score']
            ].to_html(index=False, escape=False, classes='result-table')

        else:
            avg_price_text = "<p>No results found</p>"
            table_html = ""

    return render_template(
        'index.html',
        avg_price=avg_price_text,
        table_html=table_html
    )


if __name__ == "__main__":
    app.run(debug=True)