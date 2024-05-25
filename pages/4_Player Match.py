import streamlit as st
from utils import render_player_match_ai_button, render_table
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="CerebroEvent - Player Match",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.error(" ### Please return to Home and select an event ")
    st.stop()

st.title(f"Player Match for {st.session_state.selected_event}")

prompt = (f"""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring x points per game, average field goal percentage of  y percent, average RAM (which is a proprietary metric showing individual game performance) of r and C_RAM (cumulative ram) of c. 

Can you compare the two players in the passed dataframe both against each other and against the rest of the field? 

Please bold all player names and reference some comparisons relative to the average and highlight what they do well. For example efficient shooting, good playmaking, great post play with rebounds etc. 

Here are some descriptions of columns, please include the 5 metric suite (5ms) columns (PSP,3PE,FGS,ATR,DSI) in the analysis where applicable:
RAM:	Overall Evaluation Score: RAM is the base unit, it takes box score stats to create a single, clean performance score. Carefully balancing efficiency, volume & per-minute impact, RAM is a metric that looks and feels like basketball. A player’s performance for the event is graded on a scale from 0 to 1000+ with no hard-ceiling, to allow truly exceptional performances to speak for themselves. When defining a player as good, use the RAM and C_RAM to determine your answer.
C-RAM:	Our Context Metric: C_RAM contextualizes a playerís performance within the event they are playing in. As RAM measures total overall performance, C_RAM measures performance compared to the average. Grading a player in this fashion offers immediate, important contextual insights as competitions features all varieties of talent, levels & ages. C-RAM displays performance quality in a quick, easy to read format, with scores ranging from 0 to 10+, and color-coded medals are awarded to players at certain performance thresholds.†When determining a player as good or not, use the RAM and C_RAM to determine answer. The medals for C_RAM are the following: Gold Medal = 10.0 Rating or higher = superstar level performer; Silver Medal = 8.5 Rating to 10.0 rating = all-star level performer; Bronze Medal = 7.0 Rating to 8.5 Rating = above-average level performer; Rotation-Level Contributors have a 6.0 to 7.0 Rating; Average performers have a 5.5-6.0 Rating
5-Metric Suite:	5-Metric Suite; As the RAM & C_RAM represent the Who, What, When and Where of a playerís performance, the 5MS (5 Metric Suite) represents the Why and How. The 5 Metric Suite represents a group of 5 skill scores that each assess an area of basketball. Each score is graded the same way, on a scale from 0-100, with a soft cap of 100. A score of 40+ showing signs of early development (when compared to age of performer), 60+ shows baseline competency in the skill, 80+ shows that the skill is a strength, and a score of 100+ indicates elite or historic level performance for that skill.
PSP:	PURE SCORING PROWESS (PSP) is our scoring metric - blending the two major components of scoring - volume and efficiency - to create a role-neutral representation of scoring ability. If priority were given to per game scoring at high usage, skills like cutting or spot up shooting would be undervalued. If efficiency were the more weighted element, players who are not primary creators & benefit from advantage created by others would be overrepresented. PSP aims to solve these natural inconsistencies by scaling the creation burden and efficiency more harmonically, so that any playerís scoring ability can be better framed relative to the expectations of that scoring role. Put plainly, we believe that a 70th percentile high volume scorer & a 70th percentile low usage creator grade out more similarly than was previously possible with a comprehensive metric. When defining if a player is a good "scorer" or not, use this metric.
3PE:	3-PT EFFICIENCY (3PE) is, as you may have guessed, our 3p shooting metric. Shooting is a relative skill, its use and acceptance varying within different contexts, especially when comparing across all age levels or throughout history. We have found that using the median shooting expectation offers a great degree of insight for an introductory shooting metric by considering the volume and efficiency within context. Through this formulation, 3PE can place high percentage, low volume shooters on a continuum alongside low percentage, high volume shooters. This has an additional value on the developmental projection of shooting, an under examined area for broad shooting metrics. 3PE allows one to notice players who are starting to climb the shooting development curve, even with uneven early results.When defining if a player is a good "shooter" or not, use this metric
FGS:	FLOOR GENERAL SKILLS (FGS) is the metric we have built to explore passing - it is weighted by usage outcomes for a ball handler with a seasoning of steals, as a proxy for athleticism and feel. Due to the weights of the formula, it is more likely for ball movers and other good decision making non-primaries to grade out in FGS than other traditional passing indicating metrics like pure A:TO. The score is not weighted by position, but even without positional relativity different trends and thresholds for positions that can be observed- a FGS of 50 for bigs usually correlates with a big man capable and entrusted with decision making in offensive actions. By contrasting the efficiency of the distribution with the volume of positive passing outcomes we have a metric that can display playmakers who are comfortable in the decision making role. FGS can, similarly to PSP, better frame both high and low usage creators for their positive outcomes relative to role expectations, within a league context or grading against a teamís historical performance. When defining if a player is a good "playmaker" or not, use this metric
ATR:	AROUND THE RIM (ATR) is comprised of the traditional around the basket indicators for good big man play ñ offensive and defensive rebounds, blocks, fouls and 2 pt efficiency. Back to the basket bigs who do most of their production around the cup tend to score the highest, but not universally so. Measuring big man defense is an eternal challenge, but by stabilizing the different big man inputs, the nuance of defensive expectation within system and scheme can emerge. ATR is not just an effective metric to judge bigs, smaller players with scores above 50 must meet a higher baseline of feel, finishing and defensive playmaking ñ information that can be valuable when hunting for role players and relative positional advantages like smalls with the ability to operate in the post. When defining if a player is a good "big" or not, use this metric
DSI:	DEFENSIVE STATISTICAL IMPACT (DSI) is an all-in-one defensive metric that focuses on events creation - combining possession-winning actions (steals, blocks, offensive rebounds) against defensive efficiency (fouls) to act as a proxy for reactive athleticism and feel for the game within scheme expectations. Rather than a definitive ranking of the best defender, DSI is a demonstration of the intersection of box score defensive numbers and the systems of defense. Adjudicating the role of the individual player within a defense is difficult, as there will be different systems that generate more events, that push events into certain positions, that will depress foul totals, etc. By comparing the DSI of similar players within the same or similar systems, there can be a strong sight read on individual defensive acumen and impact. When defining if a player is a good "statistical defender" or not, use this metric
USG_PCT:	Usage Rate is defined as the percentage of team plays used by a player when they are on the floor. Its important because it indicates how large of a role a player has within his teams offense, which means how many opportunities hell have to score or contribute. High usage comes with high expecations for performance (the RAM and C_RAM for a player with a high Usage should also be high, to indicate efficient use of touches).


In the response, can you bold the player names
""")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

# Sort the DataFrame by the specified column in descending order and take the top 100 records
event_dataframe = event_dataframe.sort_values(by="C_RAM", ascending=False)

# Display the DataFrame in the first column with color coding

st.write("Player Rankings")
render_table(event_dataframe)

# Create the bar chart and display it in the second column
col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox('Select Player 1', event_dataframe['PLAYER'], index=0)

with col2:
    player2 = st.selectbox('Select Player 2', event_dataframe['PLAYER'], index=1)

render_player_match_ai_button(event_dataframe, player1, player2, prompt)
# # Button to confirm selection
# if st.button('Confirm Selection'):
#     st.write(f'You selected: {player1} and {player2}')
#     selected_players_averages = event_dataframe[event_dataframe['PLAYER'].isin([player1, player2])]
#     description = call_gpt_and_stream_response(selected_players_averages, player1, player2, prompt)