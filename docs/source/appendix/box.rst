.. _appendix_box:

Box
===

Rich defines a number of ways of drawing boxes and lines such as those used in tables. To select a box style import one of the constants below from rich.box. For example::

    from rich import box
    table = Table(box=box.SQUARE)

The constants are as follows:

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800080">         box.ASCII          </span>
    +-------------------------+
    |<span style="color: #7f7f7f; font-weight: bold">            </span>|<span style="color: #7f7f7f; font-weight: bold">            </span>|
    |------------+------------|
    |<span style="color: #7f7f7f">            </span>|<span style="color: #7f7f7f">            </span>|
    |------------+------------|
    |<span style="color: #7f7f7f; font-weight: bold">            </span>|<span style="color: #7f7f7f; font-weight: bold">            </span>|
    +-------------------------+
    <span style="color: #800080">         box.SQUARE         </span>
    ┌────────────┬────────────┐
    │<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>│
    ├────────────┼────────────┤
    │<span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span>│
    ├────────────┼────────────┤
    │<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>│
    └────────────┴────────────┘
    <span style="color: #800080">        box.MINIMAL         </span>
                            
    <span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span> 
    ────────────┼──────────── 
    <span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span> 
    ────────────┼──────────── 
    <span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span> 
                            
    <span style="color: #800080">   box.MINIMAL_HEAVY_HEAD   </span>
                            
    <span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span> 
    ━━━━━━━━━━━━┿━━━━━━━━━━━━ 
    <span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span> 
    ────────────┼──────────── 
    <span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span> 
                            
    <span style="color: #800080">  box.MINIMAL_DOUBLE_HEAD   </span>
                            
    <span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span> 
    ════════════╪════════════ 
    <span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span> 
    ────────────┼──────────── 
    <span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span> 
                            
    <span style="color: #800080">         box.SIMPLE         </span>
                            
    <span style="color: #7f7f7f; font-weight: bold">            </span> <span style="color: #7f7f7f; font-weight: bold">            </span> 
    ───────────────────────────
    <span style="color: #7f7f7f">            </span> <span style="color: #7f7f7f">            </span> 
    ───────────────────────────
    <span style="color: #7f7f7f; font-weight: bold">            </span> <span style="color: #7f7f7f; font-weight: bold">            </span> 
                            
    <span style="color: #800080">      box.SIMPLE_HEAVY      </span>
                            
    <span style="color: #7f7f7f; font-weight: bold">            </span> <span style="color: #7f7f7f; font-weight: bold">            </span> 
    ╺━━━━━━━━━━━━━━━━━━━━━━━━━╸
    <span style="color: #7f7f7f">            </span> <span style="color: #7f7f7f">            </span> 
    ╺━━━━━━━━━━━━━━━━━━━━━━━━━╸
    <span style="color: #7f7f7f; font-weight: bold">            </span> <span style="color: #7f7f7f; font-weight: bold">            </span> 
                            
    <span style="color: #800080">      box.HORIZONTALS       </span>
    ───────────────────────────
    <span style="color: #7f7f7f; font-weight: bold">            </span> <span style="color: #7f7f7f; font-weight: bold">            </span> 
    ───────────────────────────
    <span style="color: #7f7f7f">            </span> <span style="color: #7f7f7f">            </span> 
    ───────────────────────────
    <span style="color: #7f7f7f; font-weight: bold">            </span> <span style="color: #7f7f7f; font-weight: bold">            </span> 
    ───────────────────────────
    <span style="color: #800080">        box.ROUNDED         </span>
    ╭────────────┬────────────╮
    │<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>│
    ├────────────┼────────────┤
    │<span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span>│
    ├────────────┼────────────┤
    │<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>│
    ╰────────────┴────────────╯
    <span style="color: #800080">         box.HEAVY          </span>
    ┏━━━━━━━━━━━━┳━━━━━━━━━━━━┓
    ┃<span style="color: #7f7f7f; font-weight: bold">            </span>┃<span style="color: #7f7f7f; font-weight: bold">            </span>┃
    ┣━━━━━━━━━━━━╋━━━━━━━━━━━━┫
    ┃<span style="color: #7f7f7f">            </span>┃<span style="color: #7f7f7f">            </span>┃
    ┣━━━━━━━━━━━━╋━━━━━━━━━━━━┫
    ┃<span style="color: #7f7f7f; font-weight: bold">            </span>┃<span style="color: #7f7f7f; font-weight: bold">            </span>┃
    ┗━━━━━━━━━━━━┻━━━━━━━━━━━━┛
    <span style="color: #800080">       box.HEAVY_EDGE       </span>
    ┏━━━━━━━━━━━━┯━━━━━━━━━━━━┓
    ┃<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>┃
    ┠────────────┼────────────┨
    ┃<span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span>┃
    ┠────────────┼────────────┨
    ┃<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>┃
    ┗━━━━━━━━━━━━┷━━━━━━━━━━━━┛
    <span style="color: #800080">       box.HEAVY_HEAD       </span>
    ┏━━━━━━━━━━━━┳━━━━━━━━━━━━┓
    ┃<span style="color: #7f7f7f; font-weight: bold">            </span>┃<span style="color: #7f7f7f; font-weight: bold">            </span>┃
    ┡━━━━━━━━━━━━╇━━━━━━━━━━━━┩
    │<span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span>│
    ├────────────┼────────────┤
    │<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>│
    └────────────┴────────────┘
    <span style="color: #800080">         box.DOUBLE         </span>
    ╔════════════╦════════════╗
    ║<span style="color: #7f7f7f; font-weight: bold">            </span>║<span style="color: #7f7f7f; font-weight: bold">            </span>║
    ╠════════════╬════════════╣
    ║<span style="color: #7f7f7f">            </span>║<span style="color: #7f7f7f">            </span>║
    ╠════════════╬════════════╣
    ║<span style="color: #7f7f7f; font-weight: bold">            </span>║<span style="color: #7f7f7f; font-weight: bold">            </span>║
    ╚════════════╩════════════╝
    <span style="color: #800080">      box.DOUBLE_EDGE       </span>
    ╔════════════╤════════════╗
    ║<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>║
    ╟────────────┼────────────╢
    ║<span style="color: #7f7f7f">            </span>│<span style="color: #7f7f7f">            </span>║
    ╟────────────┼────────────╢
    ║<span style="color: #7f7f7f; font-weight: bold">            </span>│<span style="color: #7f7f7f; font-weight: bold">            </span>║
    ╚════════════╧════════════╝
    </pre>