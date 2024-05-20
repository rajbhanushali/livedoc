import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from utils import get_dataframe_description
from utils import *
# Create the DataFrame
st.set_page_config(
    page_title="Cerebro Event Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Title of the page
st.title("Overview of EYBL")

# Display total players and average RAM using columns
col1, col2 = st.columns(2)
col1.metric("Total Players", "323")
col2.metric("Average RAM", "405")
data = {
    'RANK': range(1, 11),
    'PLAYER': [
        'Cameron Boozer', 'Cayden Boozer', 'Jaylen Harrell', 'William Riley', 
        'Adlan Elamin', 'Kedrick Simmons', 'Jaylen Cross', 'Cooper Flagg', 
        'Isaiah Henry', 'Alexander Lloyd'
    ],
    'TEAM': [
        'Nightrydas Elite (16U)', 'Nightrydas Elite (16U)', 'Expressions (16U)', 'UPlay (16U)', 
        'Team Takeover (16U)', 'Team Thad (16U)', 'Team CP3 (16U)', 'Maine United (16U)', 
        'Team CP3 (16U)', 'Nightrydas Elite (16U)'
    ],
    'W%': [1.000, 1.000, 0.800, 0.750, 0.800, 0.750, 0.800, 0.250, 0.800, 1.000],
    'C-RAM': [17.3, 11.2, 10.9, 10.4, 10.0, 9.8, 8.8, 13.6, 8.7, 7.9],
    'MOP SCORE': [229, 130, 113, 103, 101, 94, 85, 84, 83, 82]
}

df = pd.DataFrame(data)
fulldf= df.merge(eybl, on='PLAYER', how='inner')
#st.write(fulldf)



# Pie chart data
total_performers = 323
categories = ['Gold', 'Silver', 'Bronze', 'Not Rated']
not_rated = total_performers - (gold + silver + bronze)
values = [gold, silver, bronze, not_rated]
colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#808080']  # Adjusted colors for contrast








# Layout for table and pie chart
left_column, right_column = st.columns([1, .5])
with left_column:
    st.markdown(table_html, unsafe_allow_html=True)
with right_column:
    # Plot the pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=categories, colors=colors, startangle=90,
                                      autopct='%1.1f%%', pctdistance=1.2)
    # Draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Change autotexts properties
    for autotext in autotexts:
        autotext.set_color('black')
    
    plt.setp(texts, weight="bold")
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)


def plot_bar_chart(dataframe):
    fig = px.bar(
        dataframe,
        x="C-RAM",
        y="PLAYER",
        orientation='h',
        title="Top Players by C-RAM Score",
        color='C-RAM',
        color_continuous_scale='viridis',
        labels={'C-RAM': 'C-RAM Score', 'Name': 'Player Name'},
        template='plotly_white'
    )
    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig)
df2 = pd.read_csv("EYBL.csv")
df2 = df2.nlargest(20, 'C-RAM')[['PLAYER', 'C-RAM']]
plot_bar_chart(df2)    
# Descriptive text blurb
# st.write("""
# ### Breakdown of EYBL Event Performers
# In the EYBL event, we categorize performers into tiers based on their C-RAM scores. 
# Gold tier represents the elite performers, Silver tier indicates the proficient ones, 
# and Bronze tier includes developing talents. Performers not falling into these tiers 
# are classified as 'Not Rated'. This categorization helps in the assessment and 
# further development of players. The pie chart to the right visually represents the 
# distribution of these tiers among a total of 323 performers.
# """)

# The command below is used to run the streamlit app from the script, typically used in the terminal.
# st.run()
prompt = (f"""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring {ppg} points per game, average field goal percentage of {fg_pct} percent, average RAM (which is a proprietary metric showing individual game performance) of {ram} and C_RAM (cumulative ram) of {c_ram}. Can you take this table and describe the top players performances relative to the averages

Here is an example of a "good description": This event contained 323 players across X teams, with players averaging X ppg, X FG%, and X RAM. The most notable performance in the event came from Player X (this will be calculated based on highest game RAM, played at least 24 min) who had statistics of X, Y, and Z (show the best stats of the player here, traditional not cerebro metrics). Team Y had the most wins in the event, with their leading player X averaging A, B and C. 

In the response, can you bold the player names

Here are some descriptions of columns, please include the 5 metric suite (5ms) columns (PSP,3PE,FGS,ATR,DSI) in the analysis where applicable:
RAM:	Overall Evaluation Score: RAM is the base unit, it takes box score stats to create a single, clean performance score. Carefully balancing efficiency, volume & per-minute impact, RAM is a metric that looks and feels like basketball. A player’s performance for the event is graded on a scale from 0 to 1000+ with no hard-ceiling, to allow truly exceptional performances to speak for themselves. When defining a player as good, use the RAM and C_RAM to determine your answer.
C_RAM:	Our Context Metric: C_RAM contextualizes a playerís performance within the event they are playing in. As RAM measures total overall performance, C_RAM measures performance compared to the average. Grading a player in this fashion offers immediate, important contextual insights as competitions features all varieties of talent, levels & ages. C-RAM displays performance quality in a quick, easy to read format, with scores ranging from 0 to 10+, and color-coded medals are awarded to players at certain performance thresholds.†When determining a player as good or not, use the RAM and C_RAM to determine answer. The medals for C_RAM are the following: Gold Medal = 10.0 Rating or higher = superstar level performer; Silver Medal = 8.5 Rating to 10.0 rating = all-star level performer; Bronze Medal = 7.0 Rating to 8.5 Rating = above-average level performer; Rotation-Level Contributors have a 6.0 to 7.0 Rating; Average performers have a 5.5-6.0 Rating
5-Metric Suite:	5-Metric Suite; As the RAM & C_RAM represent the Who, What, When and Where of a playerís performance, the 5MS (5 Metric Suite) represents the Why and How. The 5 Metric Suite represents a group of 5 skill scores that each assess an area of basketball. Each score is graded the same way, on a scale from 0-100, with a soft cap of 100. A score of 40+ showing signs of early development (when compared to age of performer), 60+ shows baseline competency in the skill, 80+ shows that the skill is a strength, and a score of 100+ indicates elite or historic level performance for that skill.
PSP:	PURE SCORING PROWESS (PSP) is our scoring metric - blending the two major components of scoring - volume and efficiency - to create a role-neutral representation of scoring ability. If priority were given to per game scoring at high usage, skills like cutting or spot up shooting would be undervalued. If efficiency were the more weighted element, players who are not primary creators & benefit from advantage created by others would be overrepresented. PSP aims to solve these natural inconsistencies by scaling the creation burden and efficiency more harmonically, so that any playerís scoring ability can be better framed relative to the expectations of that scoring role. Put plainly, we believe that a 70th percentile high volume scorer & a 70th percentile low usage creator grade out more similarly than was previously possible with a comprehensive metric. When defining if a player is a good "scorer" or not, use this metric.
3PE:	3-PT EFFICIENCY (3PE) is, as you may have guessed, our 3p shooting metric. Shooting is a relative skill, its use and acceptance varying within different contexts, especially when comparing across all age levels or throughout history. We have found that using the median shooting expectation offers a great degree of insight for an introductory shooting metric by considering the volume and efficiency within context. Through this formulation, 3PE can place high percentage, low volume shooters on a continuum alongside low percentage, high volume shooters. This has an additional value on the developmental projection of shooting, an under examined area for broad shooting metrics. 3PE allows one to notice players who are starting to climb the shooting development curve, even with uneven early results.When defining if a player is a good "shooter" or not, use this metric
FGS:	FLOOR GENERAL SKILLS (FGS) is the metric we have built to explore passing - it is weighted by usage outcomes for a ball handler with a seasoning of steals, as a proxy for athleticism and feel. Due to the weights of the formula, it is more likely for ball movers and other good decision making non-primaries to grade out in FGS than other traditional passing indicating metrics like pure A:TO. The score is not weighted by position, but even without positional relativity different trends and thresholds for positions that can be observed- a FGS of 50 for bigs usually correlates with a big man capable and entrusted with decision making in offensive actions. By contrasting the efficiency of the distribution with the volume of positive passing outcomes we have a metric that can display playmakers who are comfortable in the decision making role. FGS can, similarly to PSP, better frame both high and low usage creators for their positive outcomes relative to role expectations, within a league context or grading against a teamís historical performance. When defining if a player is a good "playmaker" or not, use this metric
ATR:	AROUND THE RIM (ATR) is comprised of the traditional around the basket indicators for good big man play ñ offensive and defensive rebounds, blocks, fouls and 2 pt efficiency. Back to the basket bigs who do most of their production around the cup tend to score the highest, but not universally so. Measuring big man defense is an eternal challenge, but by stabilizing the different big man inputs, the nuance of defensive expectation within system and scheme can emerge. ATR is not just an effective metric to judge bigs, smaller players with scores above 50 must meet a higher baseline of feel, finishing and defensive playmaking ñ information that can be valuable when hunting for role players and relative positional advantages like smalls with the ability to operate in the post. When defining if a player is a good "big" or not, use this metric
DSI:	DEFENSIVE STATISTICAL IMPACT (DSI) is an all-in-one defensive metric that focuses on events creation - combining possession-winning actions (steals, blocks, offensive rebounds) against defensive efficiency (fouls) to act as a proxy for reactive athleticism and feel for the game within scheme expectations. Rather than a definitive ranking of the best defender, DSI is a demonstration of the intersection of box score defensive numbers and the systems of defense. Adjudicating the role of the individual player within a defense is difficult, as there will be different systems that generate more events, that push events into certain positions, that will depress foul totals, etc. By comparing the DSI of similar players within the same or similar systems, there can be a strong sight read on individual defensive acumen and impact. When defining if a player is a good "statistical defender" or not, use this metric
USG_PCT:	Usage Rate is defined as the percentage of team plays used by a player when they are on the floor. Its important because it indicates how large of a role a player has within his teams offense, which means how many opportunities hell have to score or contribute. High usage comes with high expecations for performance (the RAM and C_RAM for a player with a high Usage should also be high, to indicate efficient use of touches).



""")
if st.button("AI Analysis"):
    description = get_dataframe_description(fulldf, prompt)
    st.write(description)