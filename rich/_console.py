CONSOLE_HTML_FORMAT = """\
<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<style>
{stylesheet}
body {{
    color: {foreground};
    background-color: {background};
}}
</style>
</head>
<html>
<body>
    <code>
        <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>
    </code>
</body>
</html>
"""

CONSOLE_SVG_FORMAT = """\
<svg width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {{
            font-family: "{font_family}";
            src: local("FiraCode-Regular"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
            font-style: normal;
            font-weight: 400;
        }}
        @font-face {{
            font-family: "{font_family}";
            src: local("FiraCode-Bold"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
            font-style: bold;
            font-weight: 700;
        }}
        #{wrapper_id} span {{
            display: inline-block;
            white-space: pre;
            vertical-align: top;
            font-size: {font_size}px;
            font-family:'{font_family}','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
        }}
        #{wrapper_id} a {{
            text-decoration: none;
            color: inherit;
        }}
        #{wrapper_id} .blink {{
           animation: {wrapper_id}-blinker 1s infinite;
        }}
        @keyframes {wrapper_id}-blinker {{
            from {{ opacity: 1.0; }}
            50% {{ opacity: 0.3; }}
            to {{ opacity: 1.0; }}
        }}
        #{wrapper_id} {{
            padding: {margin}px;
            padding-top: 100px;
        }}
        #{wrapper_id} #terminal {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: {theme_background_color};
            border-radius: 14px;
            outline: 1px solid #484848;
        }}
        #{wrapper_id} #terminal:after {{
            position: absolute;
            width: 100%;
            height: 100%;
            content: '';
            border-radius: 14px;
            background: rgb(71,77,102);
            background: linear-gradient(90deg, #804D69 0%, #4E4B89 100%);
            transform: rotate(-4.5deg);
            z-index: -1;
        }}
        #{wrapper_id} #terminal-header {{
            position: relative;
            width: 100%;
            background-color: #2e2e2e;
            margin-bottom: 12px;
            font-weight: bold;
            border-radius: 14px 14px 0 0;
            color: {theme_foreground_color};
            font-size: 18px;
            box-shadow: inset 0px -1px 0px 0px #4e4e4e,
                        inset 0px -4px 8px 0px #1a1a1a;
        }}
        #{wrapper_id} #terminal-title-tab {{
            display: inline-block;
            margin-top: 14px;
            margin-left: 124px;
            font-family: sans-serif;
            padding: 14px 28px;
            border-radius: 6px 6px 0 0;
            background-color: {theme_background_color};
            box-shadow: inset 0px 1px 0px 0px #4e4e4e,
                        0px -4px 4px 0px #1e1e1e,
                        inset 1px 0px 0px 0px #4e4e4e,
                        inset -1px 0px 0px 0px #4e4e4e;
        }}
        #{wrapper_id} #terminal-traffic-lights {{
            position: absolute;
            top: 24px;
            left: 20px;
        }}
        #{wrapper_id} #terminal-body {{
            line-height: {line_height}px;
            padding: 14px;
        }}
        {stylesheet}
    </style>
    <foreignObject x="0" y="0" width="100%" height="100%">
        <body xmlns="http://www.w3.org/1999/xhtml">
            <div id="{wrapper_id}">
                <div id="terminal">
                    <div id='terminal-header'>
                        <svg id="terminal-traffic-lights" width="90" height="21" viewBox="0 0 90 21" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="14" cy="8" r="8" fill="#ff6159"/>
                            <circle cx="38" cy="8" r="8" fill="#ffbd2e"/>
                            <circle cx="62" cy="8" r="8" fill="#28c941"/>
                        </svg>
                        <div id="terminal-title-tab">{title}</div>
                    </div>
                    <div id='terminal-body'>
                        {code}
                    </div>
                </div>
            </div>
        </body>
    </foreignObject>
</svg>
"""
