def get_thread_cost_string(total_cost):
    floating_box_html = (
    f"""
        <style>
        .floating-box {{
            position: fixed;
            top: 100px;
            right: 50px;  # Adjusted from 10px to 50px to move closer to center
            width: auto;
            padding: 10px;
            color: #f0f0f0;
            background-color: #000;
            border: 1px solid #ccc;
            border-radius: 5px;
            z-index: 1000;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        </style>
        <div class="floating-box">
            Updated Thread Cost: {total_cost}
        </div>
        """
    )

    return floating_box_html