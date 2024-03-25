"""
Code for plugin features related to paradox shaders
"""

import sublime
from webbrowser import open as openwebsite
from .css import CSS


def on_hover_shaders(view, point, settings, GameData):
    if settings.get("IntrinsicHoverEnabled", True) is False:
        return

    try:
        if view.syntax().name != "PdxShader":
            return
    except AttributeError:
        return

    scopesStr = view.scope_name(point)
    scopeList = scopesStr.split(" ")
    for scope in scopeList:
        if scope == "keyword.function.intrinsic.hlsl":
            posWord = view.word(point)
            intrinsicWord = view.substr(posWord)
            if intrinsicWord in GameData.IntrinsicList:
                url, desc = GameData.IntrinsicList[intrinsicWord]
                hoverBody = """
                    <body id=show-intrinsic>
                        <style>
                            %s
                        </style>
                        <p>%s</p>
                        <br>
                        <a href="%s">MSDN Link</a>
                    </body>
                """ % (
                    CSS().default,
                    desc,
                    url,
                )

                view.show_popup(
                    hoverBody,
                    flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                    location=point,
                    max_width=1024,
                    on_navigate=lambda x: openwebsite(x),
                )
                return
