import streamlit as st
import pandas as pd
import openai
import json
from openai import OpenAI
from utils import *
st.set_page_config(
    page_title="Cerebro Event Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Replace with your OpenAI API key
openai.api_key = st.secrets.OPENAI_API_KEY

client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

def get_dataframe_description(dataframe: pd.DataFrame, prompt: str) -> str:
    # Convert the DataFrame to CSV string
    dataframe_csv = dataframe.to_csv(index=False)
    
    # Prepare the message for the ChatGPT API
    messages = [
        {"role": "system", "content": "You are an NBA analyst."},
        {"role": "user", "content": f"{prompt}\n\nHere is the data:\n{dataframe_csv}"}
    ]
    
    # Send the request to the ChatGPT API
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Ensure you're using a model available in the new API
        messages=messages
    )
    
    # Extract and return the description from the response
    description = response.choices[0].message.content
    return description

# Streamlit interface
st.title("DataFrame Description with ChatGPT")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file or use the table below", type="csv")

if uploaded_file:
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
else: 
    df = pd.read_csv("EYBL.csv")

st.write("DataFrame Preview:")
st.write(df)
    
    # Input prompt
prompt = st.text_input("Enter your prompt for ChatGPT:", "Describe the data in this DataFrame.")
    
if st.button("Get Description"):
        # Get the description from ChatGPT
    description = get_dataframe_description(df, prompt)
        
        # Display the description
    st.write("Description:")
    st.write(description)

else:

    st.write("**Example prompt:**")
    st.write(f"""

    You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring {ppg} points per game, average field goal percentage of {fg_pct} percent, average RAM (which is a proprietary metric showing individual game performance) of {ram} and C_RAM (cumulative ram) of {c_ram}. Can you take this table and describe the top players performances relative to the averages

    Here is an example of a "good description": This event contained 323 players across X teams, with players averaging X ppg, X FG%, and X RAM. The most notable performance in the event came from Player X (this will be calculated based on highest game RAM, played at least 24 min) who had statistics of X, Y, and Z (show the best stats of the player here, traditional not cerebro metrics). Team Y had the most wins in the event, with their leading player X averaging A, B and C. 

    In the response, can you bold the player names

    Here are some descriptions of columns, please include the 5 metric suite (5ms) columns (PSP,3PE,FGS,ATR,DSI) in the analysis where applicable:
    #
    RAM:	Overall Evaluation Score: RAM is the base unit, it takes box score stats to create a single, clean performance score. Carefully balancing efficiency, volume & per-minute impact, RAM is a metric that looks and feels like basketball. A player’s performance for the event is graded on a scale from 0 to 1000+ with no hard-ceiling, to allow truly exceptional performances to speak for themselves. When defining a player as good, use the RAM and C_RAM to determine your answer.
    #
    C-RAM:	Our Context Metric: C_RAM contextualizes a playerís performance within the event they are playing in. As RAM measures total overall performance, C_RAM measures performance compared to the average. Grading a player in this fashion offers immediate, important contextual insights as competitions features all varieties of talent, levels & ages. C-RAM displays performance quality in a quick, easy to read format, with scores ranging from 0 to 10+, and color-coded medals are awarded to players at certain performance thresholds.†When determining a player as good or not, use the RAM and C_RAM to determine answer. The medals for C_RAM are the following: Gold Medal = 10.0 Rating or higher = superstar level performer; Silver Medal = 8.5 Rating to 10.0 rating = all-star level performer; Bronze Medal = 7.0 Rating to 8.5 Rating = above-average level performer; Rotation-Level Contributors have a 6.0 to 7.0 Rating; Average performers have a 5.5-6.0 Rating
    #
    5-Metric Suite:	5-Metric Suite; As the RAM & C_RAM represent the Who, What, When and Where of a playerís performance, the 5MS (5 Metric Suite) represents the Why and How. The 5 Metric Suite represents a group of 5 skill scores that each assess an area of basketball. Each score is graded the same way, on a scale from 0-100, with a soft cap of 100. A score of 40+ showing signs of early development (when compared to age of performer), 60+ shows baseline competency in the skill, 80+ shows that the skill is a strength, and a score of 100+ indicates elite or historic level performance for that skill.
    #
    PSP:	PURE SCORING PROWESS (PSP) is our scoring metric - blending the two major components of scoring - volume and efficiency - to create a role-neutral representation of scoring ability. If priority were given to per game scoring at high usage, skills like cutting or spot up shooting would be undervalued. If efficiency were the more weighted element, players who are not primary creators & benefit from advantage created by others would be overrepresented. PSP aims to solve these natural inconsistencies by scaling the creation burden and efficiency more harmonically, so that any playerís scoring ability can be better framed relative to the expectations of that scoring role. Put plainly, we believe that a 70th percentile high volume scorer & a 70th percentile low usage creator grade out more similarly than was previously possible with a comprehensive metric. When defining if a player is a good "scorer" or not, use this metric.
    #
    3PE:	3-PT EFFICIENCY (3PE) is, as you may have guessed, our 3p shooting metric. Shooting is a relative skill, its use and acceptance varying within different contexts, especially when comparing across all age levels or throughout history. We have found that using the median shooting expectation offers a great degree of insight for an introductory shooting metric by considering the volume and efficiency within context. Through this formulation, 3PE can place high percentage, low volume shooters on a continuum alongside low percentage, high volume shooters. This has an additional value on the developmental projection of shooting, an under examined area for broad shooting metrics. 3PE allows one to notice players who are starting to climb the shooting development curve, even with uneven early results.When defining if a player is a good "shooter" or not, use this metric
    #
    FGS:	FLOOR GENERAL SKILLS (FGS) is the metric we have built to explore passing - it is weighted by usage outcomes for a ball handler with a seasoning of steals, as a proxy for athleticism and feel. Due to the weights of the formula, it is more likely for ball movers and other good decision making non-primaries to grade out in FGS than other traditional passing indicating metrics like pure A:TO. The score is not weighted by position, but even without positional relativity different trends and thresholds for positions that can be observed- a FGS of 50 for bigs usually correlates with a big man capable and entrusted with decision making in offensive actions. By contrasting the efficiency of the distribution with the volume of positive passing outcomes we have a metric that can display playmakers who are comfortable in the decision making role. FGS can, similarly to PSP, better frame both high and low usage creators for their positive outcomes relative to role expectations, within a league context or grading against a teamís historical performance. When defining if a player is a good "playmaker" or not, use this metric
    #
    ATR:	AROUND THE RIM (ATR) is comprised of the traditional around the basket indicators for good big man play ñ offensive and defensive rebounds, blocks, fouls and 2 pt efficiency. Back to the basket bigs who do most of their production around the cup tend to score the highest, but not universally so. Measuring big man defense is an eternal challenge, but by stabilizing the different big man inputs, the nuance of defensive expectation within system and scheme can emerge. ATR is not just an effective metric to judge bigs, smaller players with scores above 50 must meet a higher baseline of feel, finishing and defensive playmaking ñ information that can be valuable when hunting for role players and relative positional advantages like smalls with the ability to operate in the post. When defining if a player is a good "big" or not, use this metric
    #
    DSI:	DEFENSIVE STATISTICAL IMPACT (DSI) is an all-in-one defensive metric that focuses on events creation - combining possession-winning actions (steals, blocks, offensive rebounds) against defensive efficiency (fouls) to act as a proxy for reactive athleticism and feel for the game within scheme expectations. Rather than a definitive ranking of the best defender, DSI is a demonstration of the intersection of box score defensive numbers and the systems of defense. Adjudicating the role of the individual player within a defense is difficult, as there will be different systems that generate more events, that push events into certain positions, that will depress foul totals, etc. By comparing the DSI of similar players within the same or similar systems, there can be a strong sight read on individual defensive acumen and impact. When defining if a player is a good "statistical defender" or not, use this metric
    #
    USG_PCT:	Usage Rate is defined as the percentage of team plays used by a player when they are on the floor. Its important because it indicates how large of a role a player has within his teams offense, which means how many opportunities hell have to score or contribute. High usage comes with high expecations for performance (the RAM and C_RAM for a player with a high Usage should also be high, to indicate efficient use of touches).



    """)