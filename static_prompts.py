def get_overview_prompt(total_players, avg_ram, avg_cram):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has {total_players} total players, with an average RAM score of {avg_ram:.2f} and an average C_RAM score of {avg_cram:.2f}. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

        Provide a summary highlighting:
        - Notable performances from players with the highest RAM and C_RAM scores.
        - Comparison of these players' stats to the average RAM and C_RAM.
        - Insights on their scoring, shooting, playmaking, around-the-rim skills, and defensive impact using the 5 metric suite.
        - Bold the player names in your response.

        For example:
        "This event contained {total_players} players with an average RAM score of {avg_ram:.2f} and an average C_RAM score of {avg_cram:.2f}. The most notable performance came from **Player X** with a C_RAM score of 9.8, significantly above the average. **Player Y** also stood out with a PSP score of 85, indicating a strong scoring ability."

        Here are descriptions of the key metrics:
        - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
        - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
        - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
        - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
        - **FGS**: Floor General Skills, exploring passing efficiency and volume.
        - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
        - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Use this information to generate a detailed analysis of the top players' performances, and easter-egg insights into interesting statistics from the event.
    """

mop_ladder_prompt = f"""
You are a youth basketball analyst. The data in this table represents the top performers from an event. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

Provide a summary highlighting:
- Notable performances from players with the highest RAM and C_RAM scores.
- Comparison of these players' stats to the average RAM and C_RAM.
- Insights on their scoring, shooting, playmaking, around-the-rim skills, and defensive impact using the 5 metric suite.
- Bold the player names in your response.

For example:
"The most notable performance came from **Player X** with a C_RAM score of 9.8, significantly above the average. **Player Y** also stood out with a PSP score of 85, indicating a strong scoring ability." Make it very detailed and include insights on each metric and each player. Focus on box score stats also like average points per game, rebounds, shooting percentage, etc.

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
        You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring X points per game, average field goal percentage of Y percent, average RAM (which is a proprietary metric showing individual game performance) of R and C_RAM (cumulative RAM) of C.

        Compare the performances of **{player1}** and **{player2}** both against each other and against the average performance metrics. Highlight their strengths and weaknesses using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI), box score statistics, and other relevant metrics.

        Here are the key points to cover in your comparison:
        - Which player has better overall performance based on RAM and C_RAM?
        - Detailed comparison of their 5MS metrics (PSP, 3PE, FGS, ATR, DSI).
        - Insights into their scoring, shooting, playmaking, around-the-rim skills, and defensive impact.
        - Highlight any specific areas where one player excels over the other.
        - Suggest the type of team or playing style each player would fit better in.
        - Highlight their box score stats and where one outperformed the other.

        Descriptions of the key metrics:
        - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
        - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
        - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
        - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
        - **FGS**: Floor General Skills, exploring passing efficiency and volume.
        - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
        - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Please bold the player names in your response.
    """