.. _appendix_box:

Box
===

Rich has a number of constants that set the box characters used to draw tables and panels. To select a box style import one of the constants below from ``rich.box``. For example::

    from rich import box
    table = Table(box=box.SQUARE)


.. note::
    Some of the box drawing characters will not display correctly on Windows legacy terminal (cmd.exe) with *raster* fonts, and are disabled by default. If you want the full range of box options on Windows legacy terminal, use a *truetype* font and set the ``safe_box`` parameter on the Table class to ``False``.


The following table is generated with this command::

    python -m rich.box

.. raw:: html

    <pre style="font-size:90%;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #008000">╭──────────────────────────────────────────────────────────────────────────────╮</span>
    <span style="color: #008000">│</span>                                <span style="color: #008000; font-weight: bold">Box Constants</span>                                 <span style="color: #008000">│
    ╰──────────────────────────────────────────────────────────────────────────────╯</span>

    <span style="color: #800080">        box.ASCII         </span>  <span style="color: #800080">        box.SQUARE        </span>  <span style="color: #800080">      box.MINIMAL       </span>
    +------------------------+  ┌────────────┬───────────┐                          
    |<span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>|<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>|  │<span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>│   <span style="color: #7f7f7f; font-weight: bold"> Header 1  </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2 </span> 
    |------------+-----------|  ├────────────┼───────────┤   ───────────┼────────── 
    |<span style="color: #7f7f7f"> Cell       </span>|<span style="color: #7f7f7f"> Cell      </span>|  │<span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>│   <span style="color: #7f7f7f"> Cell      </span>│<span style="color: #7f7f7f"> Cell     </span> 
    |<span style="color: #7f7f7f"> Cell       </span>|<span style="color: #7f7f7f"> Cell      </span>|  │<span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>│   <span style="color: #7f7f7f"> Cell      </span>│<span style="color: #7f7f7f"> Cell     </span> 
    |------------+-----------|  ├────────────┼───────────┤   ───────────┼────────── 
    |<span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>|<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>|  │<span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>│   <span style="color: #7f7f7f; font-weight: bold"> Footer 1  </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2 </span> 
    +------------------------+  └────────────┴───────────┘                          
                                                                                    
                                                                                    
    <span style="color: #800080">  box.MINIMAL_HEAVY_HEAD  </span>  <span style="color: #800080"> box.MINIMAL_DOUBLE_HEAD  </span>  <span style="color: #800080">       box.SIMPLE       </span>
                                                                                    
     <span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>    <span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>    <span style="color: #7f7f7f; font-weight: bold"> Header 1  </span> <span style="color: #7f7f7f; font-weight: bold"> Header 2 </span> 
     ━━━━━━━━━━━━┿━━━━━━━━━━━    ════════════╪═══════════   ────────────────────────
     <span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>    <span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>    <span style="color: #7f7f7f"> Cell      </span> <span style="color: #7f7f7f"> Cell     </span> 
     <span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>    <span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>    <span style="color: #7f7f7f"> Cell      </span> <span style="color: #7f7f7f"> Cell     </span> 
     ────────────┼───────────    ────────────┼───────────   ────────────────────────
     <span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>    <span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>    <span style="color: #7f7f7f; font-weight: bold"> Footer 1  </span> <span style="color: #7f7f7f; font-weight: bold"> Footer 2 </span> 
                                                                                    
                                                                                    
                                                                                    
    <span style="color: #800080">     box.SIMPLE_HEAVY     </span>  <span style="color: #800080">     box.HORIZONTALS      </span>  <span style="color: #800080">      box.ROUNDED       </span>
                                ──────────────────────────  ╭───────────┬──────────╮
     <span style="color: #7f7f7f; font-weight: bold"> Header 1   </span> <span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>    <span style="color: #7f7f7f; font-weight: bold"> Header 1   </span> <span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>   │<span style="color: #7f7f7f; font-weight: bold"> Header 1  </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2 </span>│
    ╺━━━━━━━━━━━━━━━━━━━━━━━━╸  ──────────────────────────  ├───────────┼──────────┤
     <span style="color: #7f7f7f"> Cell       </span> <span style="color: #7f7f7f"> Cell      </span>    <span style="color: #7f7f7f"> Cell       </span> <span style="color: #7f7f7f"> Cell      </span>   │<span style="color: #7f7f7f"> Cell      </span>│<span style="color: #7f7f7f"> Cell     </span>│
     <span style="color: #7f7f7f"> Cell       </span> <span style="color: #7f7f7f"> Cell      </span>    <span style="color: #7f7f7f"> Cell       </span> <span style="color: #7f7f7f"> Cell      </span>   │<span style="color: #7f7f7f"> Cell      </span>│<span style="color: #7f7f7f"> Cell     </span>│
    ╺━━━━━━━━━━━━━━━━━━━━━━━━╸  ──────────────────────────  ├───────────┼──────────┤
     <span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span> <span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>    <span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span> <span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>   │<span style="color: #7f7f7f; font-weight: bold"> Footer 1  </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2 </span>│
                                ──────────────────────────  ╰───────────┴──────────╯
                                                                                    
                                                                                    
    <span style="color: #800080">        box.HEAVY         </span>  <span style="color: #800080">      box.HEAVY_EDGE      </span>  <span style="color: #800080">     box.HEAVY_HEAD     </span>
    ┏━━━━━━━━━━━━┳━━━━━━━━━━━┓  ┏━━━━━━━━━━━━┯━━━━━━━━━━━┓  ┏━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃<span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>┃<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>┃  ┃<span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>┃  ┃<span style="color: #7f7f7f; font-weight: bold"> Header 1  </span>┃<span style="color: #7f7f7f; font-weight: bold"> Header 2 </span>┃
    ┣━━━━━━━━━━━━╋━━━━━━━━━━━┫  ┠────────────┼───────────┨  ┡━━━━━━━━━━━╇━━━━━━━━━━┩
    ┃<span style="color: #7f7f7f"> Cell       </span>┃<span style="color: #7f7f7f"> Cell      </span>┃  ┃<span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>┃  │<span style="color: #7f7f7f"> Cell      </span>│<span style="color: #7f7f7f"> Cell     </span>│
    ┃<span style="color: #7f7f7f"> Cell       </span>┃<span style="color: #7f7f7f"> Cell      </span>┃  ┃<span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>┃  │<span style="color: #7f7f7f"> Cell      </span>│<span style="color: #7f7f7f"> Cell     </span>│
    ┣━━━━━━━━━━━━╋━━━━━━━━━━━┫  ┠────────────┼───────────┨  ├───────────┼──────────┤
    ┃<span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>┃<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>┃  ┃<span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>┃  │<span style="color: #7f7f7f; font-weight: bold"> Footer 1  </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2 </span>│
    ┗━━━━━━━━━━━━┻━━━━━━━━━━━┛  ┗━━━━━━━━━━━━┷━━━━━━━━━━━┛  └───────────┴──────────┘
                                                                                    
                                                                                    
    <span style="color: #800080">        box.DOUBLE        </span>  <span style="color: #800080">     box.DOUBLE_EDGE      </span>                          
    ╔════════════╦═══════════╗  ╔════════════╤═══════════╗                          
    ║<span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>║<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>║  ║<span style="color: #7f7f7f; font-weight: bold"> Header 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Header 2  </span>║                          
    ╠════════════╬═══════════╣  ╟────────────┼───────────╢                          
    ║<span style="color: #7f7f7f"> Cell       </span>║<span style="color: #7f7f7f"> Cell      </span>║  ║<span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>║                          
    ║<span style="color: #7f7f7f"> Cell       </span>║<span style="color: #7f7f7f"> Cell      </span>║  ║<span style="color: #7f7f7f"> Cell       </span>│<span style="color: #7f7f7f"> Cell      </span>║                          
    ╠════════════╬═══════════╣  ╟────────────┼───────────╢                          
    ║<span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>║<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>║  ║<span style="color: #7f7f7f; font-weight: bold"> Footer 1   </span>│<span style="color: #7f7f7f; font-weight: bold"> Footer 2  </span>║                          
    ╚════════════╩═══════════╝  ╚════════════╧═══════════╝                          
    </pre>   
