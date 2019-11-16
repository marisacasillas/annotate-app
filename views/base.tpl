<html>
    <head>
        <title>{{title}}</title>
        <link rel="stylesheet" type="text/css" href="/static/style/app.css">
    </head>
    <body>
        {{!base}}
        % if defined('soundmanager'):
        <script src="/static/script/soundmanager2-nodebug-jsmin.js"></script>
        % end
        <script src="/static/script/app.js"></script>
    </body>
</html>
