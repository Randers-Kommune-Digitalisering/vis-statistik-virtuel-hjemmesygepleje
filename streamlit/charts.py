import altair as alt
import pandas as pd


def create_service_pie_chart(filtered_names, filtered_visits, key, color_map):
    # Filter out names with 0 visits
    filtered_data = [(name, visits) for name, visits in zip(filtered_names, filtered_visits) if visits > 0]
    if filtered_data:
        filtered_names, filtered_visits = zip(*filtered_data)
    else:
        filtered_names, filtered_visits = [], []

    # Calculate percentages
    total_visits = sum(filtered_visits)
    percentages = [visits / total_visits * 100 for visits in filtered_visits]
    percentages = [f"{visits / total_visits * 100:.2f}%" for visits in filtered_visits]

    # Create a DataFrame
    data = pd.DataFrame({
        'Ydelse': filtered_names,
        'Antal': filtered_visits,
        'Procent': percentages,
        'colors': [color_map[name] for name in filtered_names]
    })

    # Create the pie chart
    pie_chart = alt.Chart(data).mark_arc().encode(
        theta=alt.Theta(field='Antal', type='quantitative'),
        color=alt.Color(field='Ydelse', type='nominal', scale=alt.Scale(domain=filtered_names, range=list(data['colors']))),
        tooltip=['Ydelse', 'Antal', 'Procent']
    ).properties(
        title=f'{key}',
    ).configure_title(
        fontSize=18,
        anchor='start',
        offset=5
    )

    return pie_chart, total_visits


# x and y are dicts e.g. {'axis-name': [1,2,3]} or {'axis-name': ["a", "b", "c"]}
def create_conversion_rate_bar_chart(x: dict, y: dict, min_height: float = 0.2, x_is_ou: bool = False):
    x_key = next(iter(x))
    y_key = next(iter(y))

    df = pd.DataFrame({
        f'{x_key}': x[x_key],
        f'{y_key}': y[y_key],
    })

    if x_is_ou:
        df = df.sort_values(x_key, ascending=True)
        df = df.groupby(x_key, as_index=False).sum()

    max_y = max(max(df[y_key]) * 1.5, min_height)

    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_key, sort=None, axis=alt.Axis(labelAngle=90, labelOverlap=False, title='')),
        y=alt.Y(y_key, scale=alt.Scale(domain=[0, max_y])),
        tooltip=[alt.Tooltip(x_key), alt.Tooltip(y_key, format='.2%')]
    ).properties(
        title=y_key
    )

    # Add text labels on bars
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-3  # Nudge text above bars
    ).encode(
        text=alt.Text(f'{y_key}:Q', format=',.2~%')
    )

    chart = (bars + text).configure(
        axis=alt.Axis(labelFontSize=14, titleFontSize=16, labelLimit=500),
        numberFormat='%',
        title=alt.TitleConfig(fontSize=18, anchor='start', offset=5),
    )

    return chart


# x and y are dicts e.g. {'axis-name': [1,2,3]} or {'axis-name': ["a", "b", "c"]}
def create_calls_bar_chart(x: dict, y: dict, min_height: float = 10, x_is_ou: bool = False):
    x_key = next(iter(x))
    y_key = next(iter(y))

    df = pd.DataFrame({
        f'{x_key}': x[x_key],
        f'{y_key}': y[y_key],
    })

    if x_is_ou:
        df = df.sort_values(x_key, ascending=True)
        df = df.groupby(x_key, as_index=False).sum()

    max_y = max(max(df[y_key]) * 1.5, min_height)

    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_key, sort=None, axis=alt.Axis(labelAngle=90, labelOverlap=False, title='')),
        y=alt.Y(y_key, scale=alt.Scale(domain=[0, max_y])),
        tooltip=[alt.Tooltip(x_key), alt.Tooltip(y_key)]
    ).properties(
        title=y_key
    )

    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-3
    ).encode(
        text=alt.Text(f'{y_key}:Q')
    )

    chart = (bars + text).configure(
        axis=alt.Axis(labelFontSize=14, titleFontSize=16, labelLimit=500),
        title=alt.TitleConfig(fontSize=18, anchor='start', offset=5),
    )

    return chart


# x and y are dicts e.g. {'axis-name': [1,2,3]} or {'axis-name': ["a", "b", "c"]}
def create_use_level_bar_chart(x: dict, y: dict, min_height: float = 1, x_is_ou: bool = False):
    x_key = next(iter(x))
    y_key = next(iter(y))

    df = pd.DataFrame({
        f'{x_key}': x[x_key],
        f'{y_key}': y[y_key],
    })

    if x_is_ou:
        df = df.sort_values(x_key, ascending=True)
        df = df.groupby(x_key, as_index=False).sum()

    max_y = max(max(df[y_key]) * 1.5, min_height)

    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_key, sort=None, axis=alt.Axis(labelAngle=90, labelOverlap=False, title='')),
        y=alt.Y(y_key, scale=alt.Scale(domain=[0, max_y])),
        tooltip=[alt.Tooltip(x_key), alt.Tooltip(y_key, format='.2f')]
    ).properties(
        title=y_key
    )

    # Add text labels on bars
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-3 
    ).encode(
        text=alt.Text(f'{y_key}:Q', format='.2f')
    )

    chart = (bars + text).configure(
        axis=alt.Axis(labelFontSize=14, titleFontSize=16, labelLimit=500),
        title=alt.TitleConfig(fontSize=18, anchor='start', offset=5),
    )

    return chart


def create_duration_bar_chart(x: dict, y: dict, min_height: float = 5, x_is_ou: bool = False):
    x_key = next(iter(x))
    y_key = next(iter(y))

    df = pd.DataFrame({
        f'{x_key}': x[x_key],
        f'{y_key}': y[y_key],
    })

    if x_is_ou:
        df = df.sort_values(x_key, ascending=True)
        df = df.groupby(x_key, as_index=False).sum()

    # Convert Timedelta to total seconds for plotting
    df[y_key] = df[y_key].dt.total_seconds()

    # Create a function to format the y-axis labels as mm:ss
    def format_duration(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f'{minutes:02}:{seconds:02}'

    df[y_key + '_formated'] = df[y_key].apply(format_duration)

    # Create a bar chart using Altair
    bars = alt.Chart(df).mark_bar().encode(
        x=x_key,
        y=alt.Y(f'{y_key}:Q', title=y_key, axis=alt.Axis(
            labelExpr='floor(datum.value / 60) + \':\' + (datum.value % 60 < 10 ? \'0\' : \'\') + datum.value % 60'
        )),
        tooltip=[alt.Tooltip(x_key), alt.Tooltip(f'{y_key}_formated:N', title=y_key)]
    )

    # Add text labels on bars
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-3  # Nudge text above bars
    ).encode(
        text=alt.Text(f'{y_key}_formated:N')
    )

    chart = (bars + text).configure(
        axis=alt.Axis(labelFontSize=14, titleFontSize=16, labelLimit=500),
        title=alt.TitleConfig(fontSize=18, anchor='start', offset=5),
    )

    return chart


def create_user_stat_total_graph(df, start_date, end_date):
    name = "Alle logins"

    df['tidspunkt'] = pd.to_datetime(df['tidspunkt'])

    df['dato'] = df['tidspunkt'].dt.date

    date_range = pd.date_range(start=start_date, end=end_date)
    timeunit = 'yearmonthdate'
    tooltips = [alt.Tooltip(f'{name}:Q', title='Antal Logins')]
    tooltips = tooltips + [alt.Tooltip('dato:T')]

    logins = df.groupby('dato').size().reindex(date_range, fill_value=0).reset_index(name=name)
    logins.rename(columns={'index': 'dato'}, inplace=True)

    chart = alt.Chart(logins).mark_bar(color='blue').encode(
        x=alt.X('dato:T', title='Dato', timeUnit=timeunit),
        y=alt.Y(f'{name}:Q', title=name),
        tooltip=tooltips
    ).properties(
        title='Alle logins - fordelt per dag'
    )

    return chart


def create_user_stat_unique_graph(df, start_date, end_date):
    name = "Unikke brugere"
    df['tidspunkt'] = pd.to_datetime(df['tidspunkt'])

    df['dato'] = df['tidspunkt'].dt.date

    date_range = pd.date_range(start=start_date, end=end_date)
    timeunit = 'yearmonthdate'
    tooltips = [alt.Tooltip(f'{name}:Q', title='Antal Logins')]
    tooltips = tooltips + [alt.Tooltip('dato:T')]

    logins = df.groupby('dato')['email'].nunique().reindex(date_range, fill_value=0).reset_index(name=name)

    logins.rename(columns={'index': 'dato'}, inplace=True)

    chart = alt.Chart(logins).mark_bar(color='green').encode(
        x=alt.X('dato:T', title='Date', timeUnit=timeunit),
        y=alt.Y(f'{name}:Q', title=name),
        tooltip=tooltips
    ).properties(
        title='Unikke brugere - fordelt per dag'
    )

    return chart
