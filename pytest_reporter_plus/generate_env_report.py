def write_env_html(env_info):
    html_rows = ""
    for key, value in env_info.items():
        if isinstance(value, dict):
            value_str = "<br>".join(f"{k}: {v}" for k, v in value.items())
        else:
            value_str = value
        html_rows += f"<tr><td>{key}</td><td>{value_str}</td></tr>\n"
    return f"""
    <div class="env-toggle-btn" onclick="toggleEnvSidebar()">⚙️ Env Info</div>
    <div class="env-sidebar" id="envSidebar">
        <h3>Environment Details</h3>
        <table>{html_rows}</table>
    </div>
    <script>
        function toggleEnvSidebar() {{
            const sidebar = document.getElementById("envSidebar");
            sidebar.classList.toggle("active");
        }}
    </script>
    """