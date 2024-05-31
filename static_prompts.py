def get_overview_prompt(total_players, avg_ram, avg_cram):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has {total_players} total players, with an average RAM score of {avg_ram} and an average C_RAM score of {avg_cram}. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

        Here are descriptions of the key metrics:
        - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
        - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
        - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
        - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
        - **FGS**: Floor General Skills, exploring passing efficiency and volume.
        - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
        - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Provide a summary highlighting the following sections:

        **Brief Introduductive Paragraph**
        - In paragraph natural text, give a summary of the event using total players, average RAM/CRAM, and top performers at each of the 5 metric suite,

        **Impressive Performances**
        - Comparison of notable performer's statistics to the average RAM and C_RAM.
        - Key players who lead in box score stats such as points, rebounds, assists, steals, and blocks.
        - Efficiency of the best players using fg_pct, three_pt_pct, and free_throw_pct
        - Detailed analysis using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

        **Interesting (Easter Egg) Statistics**
        - Highlight unique or surprising stats from the event.
        - Provide insights into specific players' standout performances or anomalies. 

        Use this information to generate a detailed analysis of the top players' performances, and easter-egg insights into interesting statistics from the event, following the required sections.
    """

player_report_prompt = f"""
  You are a youth basketball analyst. The data in this table represents a single performer from an event. Analyze the players' performance and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

  Here are descriptions of the key metrics:
  - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
  - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
  - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
  - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
  - **FGS**: Floor General Skills, exploring passing efficiency and volume.
  - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
  - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

  Provide a summary highlighting the following sections:

  **PLayer Summary**
  - In paragraph natural text, give a summary of the player and his stats, outlining box score and 5ms.
  - Include Efficiency using fg_pct, three_pt_pct, and free_throw_pct
  - Highlight strengths, weaknesses, and type of what kind of team they would best fit in / succeed with in its own paragraph. 
  
  **Interesting (Easter Egg) Statistics**
  - Highlight unique or surprising stats from the player.

"""

def get_player_match_prompt(player1, player2):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. 

        Here are descriptions of the key metrics:
          - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
          - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
          - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
          - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
          - **FGS**: Floor General Skills, exploring passing efficiency and volume.
          - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
          - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Compare the performances of **{player1}** and **{player2}** both against each other and against the average performance metrics. Highlight their strengths and weaknesses using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI), box score statistics, and other relevant metrics.

        **Comparison Overview**
        - Begin with a clear, introductive paragraph that is comprehensive about these players and how they perform against each other, and against the field based on their 5MS and box score stats like points, rebounds, assists, steals, blocks, and efficiency measured with PCT. 

        - **Strengths and Weaknesses**
          - Highlight any specific areas where one player excels over the other.

        - **Team Fit and Playing Style**
          - Suggest the type of team or playing style each player would fit better in.

        Please bold the player names in your response.
    """

def get_skill_leader_prompt(skill, event):
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the {event} tournament.
        Here are descriptions of the key metrics:
          - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
          - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
          - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
          - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
          - **FGS**: Floor General Skills, exploring passing efficiency and volume.
          - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
          - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Based on the column {skill}, generate a summary for the leaders of that stat. Follow the format below:

        **Comprehensive overview**
        - In paragraph natural text, give a summary of the players that were exceptional at the relevant skill selected, and examples of their success using the box score stats like efficiency (measured in PCT), points, rebounds, assists, steals, and blocks. Give at least the top 5 players in the selected skill.
        - Make sure this summary is comparative in nature as well, outlining how well someone performed compared to another player and how the other player might be better at a different skill or fit with a different kind of team based on the highlighted skills.

        Use this format to generate a detailed summary of the leaders in the {skill} stat.
    """

def get_comparative_prompt(players, event):
    player_list = ", ".join([f"**{player}**" for player in players])
    return f"""
        You are a youth basketball analyst. The data in this table represents the top performers from the {event} tournament.

        Here are descriptions of the key metrics:
          - **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
          - **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
          - **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
          - **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
          - **FGS**: Floor General Skills, exploring passing efficiency and volume.
          - **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
          - **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

        Compare the performances of {player_list} against each other and against the average performance metrics. Highlight their strengths and weaknesses using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI), box score statistics, and other relevant metrics.

        **Comparison Overview**
        - Begin with a clear, introductive paragraph that is comprehensive about these players and how they perform against each other, and against the field based on their 5MS and box score stats like points, rebounds, assists, steals, blocks, and efficiency measured with PCT. 

        - **Strengths and Weaknesses**
          - Highlight any specific areas where one player excels over the other.

        - **Team Fit and Playing Style**
          - Suggest the type of team or playing style each player would fit better in.

        Please bold the player names in your response. I don't want to just see their stats, but instead receive an interesting analysis of who was better at what and how that defines their abilities

    """
