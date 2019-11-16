<html>
    <head>
        <title>{{title}}</title>
        <link rel="stylesheet" type="text/css" href="/static/style/app.css">
    </head>
    <body>
        {{!base}}
        % if defined('audio'):
        <script src="/static/script/howler.min.js"></script>
        % end
        <script src="/static/script/app.js"></script>
    </body>
</html>
