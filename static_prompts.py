def get_overview_prompt(total_players, avg_ram, avg_cram):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has {total_players} total players, with an average RAM score of {avg_ram:.2f} and an average C_RAM score of {avg_cram:.2f}. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

        Provide a summary highlighting the following sections:

        **Event Description and Highlights**
        - Total players: {total_players}
        - Average RAM score: {avg_ram:.2f}
        - Average C_RAM score: {avg_cram:.2f}

        **Impressive Performances**
        - Notable performances from players with the highest RAM and C_RAM scores.
        - Comparison of these players' stats to the average RAM and C_RAM.
        - Key players who lead in box score stats such as points, rebounds, assists, and blocks.
        - Detailed analysis using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

        **Interesting (Easter Egg) Statistics**
        - Highlight unique or surprising stats from the event.
        - Provide insights into specific players' standout performances or anomalies.

        Here are descriptions of the key metrics:
        - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
        - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
        - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
        - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
        - **FGS**: Floor General Skills, exploring passing efficiency and volume.
        - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
        - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Use this information to generate a detailed analysis of the top players' performances, and easter-egg insights into interesting statistics from the event, following the required sections.
    """

mop_ladder_prompt = f"""
You are a youth basketball analyst. The data in this table represents the top performers from an event. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

Provide a summary highlighting:
- Notable performances from players with the highest RAM and C_RAM scores.
- Comparison of these players' stats to the average RAM and C_RAM.
- Insights on their scoring, shooting, playmaking, around-the-rim skills, and defensive impact using the 5 metric suite.
- Bold the player names in your response.

**Interesting Statistics**
- Highlight unique or surprising stats from the top players in the event.
- Provide insights into specific players' standout performances or anomalies.

Here are descriptions of the key metrics:
- **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
- **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
- **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
- **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
- **FGS**: Floor General Skills, exploring passing efficiency and volume.
- **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
- **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

Use this information to generate a detailed analysis of the top players' performances. Focus on comparisons between the players and highlighting strengths in one where a different player has a weakness, etc.
"""

def get_player_match_prompt(player1, player2):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams, with average performers scoring X points per game, an average field goal percentage of Y percent, an average RAM (which is a proprietary metric showing individual game performance) of R, and a C_RAM (cumulative RAM) of C.

        Compare the performances of **{player1}** and **{player2}** both against each other and against the average performance metrics. Highlight their strengths and weaknesses using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI), box score statistics, and other relevant metrics.

        **Comparison Overview**
        - Total players: 323
        - Teams: 32
        - Average points per game: X
        - Average field goal percentage: Y%
        - Average RAM: R
        - Average C_RAM: C

        **Player Comparison**
        - **Overall Performance**
          - Which player has better overall performance based on RAM and C_RAM?

        - **5 Metric Suite (5MS) Comparison**
          - Detailed comparison of their metrics (PSP, 3PE, FGS, ATR, DSI).

        - **Box Score Statistics**
          - Insights into their scoring, shooting, playmaking, around-the-rim skills, and defensive impact.

        - **Strengths and Weaknesses**
          - Highlight any specific areas where one player excels over the other.

        - **Team Fit and Playing Style**
          - Suggest the type of team or playing style each player would fit better in.

        **Example Format:**
        This tournament had 323 players across 32 teams, with average performers scoring X points per game and an average field goal percentage of Y percent. The average RAM was R, and the average C_RAM was C.

        **Comparison Overview**
        - **{player1}** vs. **{player2}**:
          - **{player1}** has a higher RAM of 850 compared to **{player2}**'s RAM of 780.
          - In terms of C_RAM, **{player1}** scores a 9.2, which is above **{player2}**'s score of 8.5.

        **5 Metric Suite (5MS) Comparison**
        - **{player1}** excels in PSP with a score of 90, indicating superior scoring ability.
        - **{player2}** leads in 3PE with an efficiency of 45%, demonstrating better shooting from beyond the arc.

        **Box Score Statistics**
        - **{player1}** averages 20 points per game, 8 rebounds, and 5 assists, with a shooting percentage of 50%.
        - **{player2}** averages 18 points per game, 7 rebounds, and 6 assists, with a shooting percentage of 47%.

        **Strengths and Weaknesses**
        - **{player1}** excels in around-the-rim play (ATR) with a score of 85, while **{player2}** shows strengths in defensive impact (DSI) with a score of 80.

        **Team Fit and Playing Style**
        - **{player1}** would be an excellent fit for a team that focuses on inside scoring and rebounding.
        - **{player2}** would thrive in a team that emphasizes perimeter shooting and playmaking.

        **Descriptions of the Key Metrics:**
        - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
        - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
        - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
        - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
        - **FGS**: Floor General Skills, exploring passing efficiency and volume.
        - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
        - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Please bold the player names in your response.
    """

def get_skill_leader_prompt(skill, event):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the {event} tournament. The tournament features various teams and players, with average performers scoring a certain number of points per game, maintaining an average field goal percentage, and having average RAM (a proprietary metric showing individual game performance) and C_RAM (cumulative RAM) scores.

        Based on the column {skill}, generate a summary for the leaders of that stat. Follow the format below:

        **Event Overview**
        - Number of players: [total players]
        - Number of teams: [total teams]
        - Average points per game: [average points per game]
        - Average field goal percentage: [average field goal percentage]
        - Average RAM: [average RAM]
        - Average C_RAM: [average C_RAM]

        **Skill Leaders in {skill}**
        - **Top Performer:**
          - [Top Player Name] led the event in {skill}, scoring [Skill Score], which was [Percentage above average] better than the average. He averaged [Stat 1], [Stat 2], and [Stat 3]. He accounted for [Percentage of team contribution] of his team's overall [relevant stat] and led the event with [Total Stat].

        - **Second Performer:**
          - [Second Player Name] from [Second Player Team], with a {skill} score of [Second Skill Score], averaged [Stat 1], [Stat 2], and [Stat 3]. His key outlier stat is [Outlier Stat].

        **Example Summary Format:**
        The {event} tournament featured [total players] players from [total teams] teams. The average player scored [average points per game] points per game and had a field goal percentage of [average field goal percentage]%. The average RAM was [average RAM], and the average C_RAM was [average C_RAM].

        **Skill Leaders in {skill}:**
        - **[Top Player Name]** led the event in {skill} with a score of [Skill Score], which was [Percentage above average]% above the average. He averaged [Stat 1], [Stat 2], and [Stat 3]. He contributed to [Percentage of team contribution]% of his team's [relevant stat] and led the event with [Total Stat].
        - Trailing him in our {skill} leaderboard was **[Second Player Name]** from [Second Player Team], who had a {skill} score of [Second Skill Score] and averaged [Stat 1], [Stat 2], and [Stat 3]. His key outlier stat is [Outlier Stat].

        Use this format to generate a detailed summary of the leaders in the {skill} stat.
    """

def get_top20_prompt(players, event):
    player_list = ", ".join([f"**{player}**" for player in players])
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the {event} tournament. The tournament features various teams and players, with average performers scoring a certain number of points per game, maintaining an average field goal percentage, and having average RAM (a proprietary metric showing individual game performance) and C_RAM (cumulative RAM) scores.

        Compare {player_list} to the rest of the field. Discuss their key metrics as defined below:

        Highlight the metrics where {player_list} excel relative to the field.

        **Comparison of {player_list} to the Field:**
        Discuss how each player's performances compare to each other and highlight their standout metrics.
        Explain box score stats and highlight who averaged more at what (like points, rebounds, assists, blocks, steals, etc), and what that means about them as a player. 
        I don't want to see their stats, but instead an interesting analysis of who was better at what and how that defines their abilities
    """