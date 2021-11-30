.. _appendix-styles:

Default Styles
==============

A list of all the available styles provided in the default Theme.

You can also produce this table by running the following command::

    python -m rich.default_styles

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃<span style="font-weight: bold"> Name                          </span>┃<span style="font-weight: bold"> Styling                            </span>┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ none                          │ none                               │
    │ <span style="color: #000000; text-decoration-color: #000000; background-color: #ffffff">reset                        </span> │ not bold not dim not italic not    │
    │                               │ underline not blink not blink2 not │
    │                               │ reverse not conceal not strike     │
    │                               │ default on default                 │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">dim                          </span> │ dim                                │
    │ bright                        │ not dim                            │
    │ <span style="font-weight: bold">bold                         </span> │ bold                               │
    │ <span style="font-weight: bold">strong                       </span> │ bold                               │
    │ <span style="font-weight: bold">code                         </span> │ bold reverse                       │
    │ <span style="font-style: italic">italic                       </span> │ italic                             │
    │ <span style="font-style: italic">emphasize                    </span> │ italic                             │
    │ <span style="text-decoration: underline">underline                    </span> │ underline                          │
    │ blink                         │ blink                              │
    │ blink2                        │ blink2                             │
    │ reverse                       │ reverse                            │
    │ <span style="text-decoration: line-through">strike                       </span> │ strike                             │
    │ <span style="color: #000000; text-decoration-color: #000000">black                        </span> │ black                              │
    │ <span style="color: #800000; text-decoration-color: #800000">red                          </span> │ red                                │
    │ <span style="color: #008000; text-decoration-color: #008000">green                        </span> │ green                              │
    │ <span style="color: #808000; text-decoration-color: #808000">yellow                       </span> │ yellow                             │
    │ <span style="color: #800080; text-decoration-color: #800080">magenta                      </span> │ magenta                            │
    │ <span style="color: #008080; text-decoration-color: #008080">cyan                         </span> │ cyan                               │
    │ <span style="color: #c0c0c0; text-decoration-color: #c0c0c0">white                        </span> │ white                              │
    │ <span style="color: #808000; text-decoration-color: #808000; font-style: italic">inspect.attr                 </span> │ italic yellow                      │
    │ <span style="color: #bfbf7f; text-decoration-color: #bfbf7f; font-style: italic">inspect.attr.dunder          </span> │ dim italic yellow                  │
    │ <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">inspect.callable             </span> │ bold red                           │
    │ <span style="color: #00ffff; text-decoration-color: #00ffff; font-style: italic">inspect.def                  </span> │ italic bright_cyan                 │
    │ <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">inspect.error                </span> │ bold red                           │
    │ inspect.equals                │ none                               │
    │ <span style="color: #008080; text-decoration-color: #008080">inspect.help                 </span> │ cyan                               │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">inspect.doc                  </span> │ dim                                │
    │ <span style="color: #008000; text-decoration-color: #008000">inspect.value.border         </span> │ green                              │
    │ <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">live.ellipsis                </span> │ bold red                           │
    │ <span style="color: #800000; text-decoration-color: #800000">layout.tree.row              </span> │ not dim red                        │
    │ <span style="color: #000080; text-decoration-color: #000080">layout.tree.column           </span> │ not dim blue                       │
    │ <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">logging.keyword              </span> │ bold yellow                        │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">logging.level.notset         </span> │ dim                                │
    │ <span style="color: #008000; text-decoration-color: #008000">logging.level.debug          </span> │ green                              │
    │ <span style="color: #000080; text-decoration-color: #000080">logging.level.info           </span> │ blue                               │
    │ <span style="color: #800000; text-decoration-color: #800000">logging.level.warning        </span> │ red                                │
    │ <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">logging.level.error          </span> │ bold red                           │
    │ <span style="background-color: #800000; font-weight: bold">logging.level.critical       </span> │ bold reverse red                   │
    │ log.level                     │ none                               │
    │ <span style="color: #7fbfbf; text-decoration-color: #7fbfbf">log.time                     </span> │ dim cyan                           │
    │ log.message                   │ none                               │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">log.path                     </span> │ dim                                │
    │ <span style="color: #808000; text-decoration-color: #808000">repr.ellipsis                </span> │ yellow                             │
    │ <span style="color: #7fbf7f; text-decoration-color: #7fbf7f">repr.indent                  </span> │ dim green                          │
    │ <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">repr.error                   </span> │ bold red                           │
    │ <span style="color: #008000; text-decoration-color: #008000">repr.str                     </span> │ not bold not italic green          │
    │ <span style="font-weight: bold">repr.brace                   </span> │ bold                               │
    │ <span style="font-weight: bold">repr.comma                   </span> │ bold                               │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00; font-weight: bold">repr.ipv4                    </span> │ bold bright_green                  │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00; font-weight: bold">repr.ipv6                    </span> │ bold bright_green                  │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00; font-weight: bold">repr.eui48                   </span> │ bold bright_green                  │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00; font-weight: bold">repr.eui64                   </span> │ bold bright_green                  │
    │ <span style="font-weight: bold">repr.tag_start               </span> │ bold                               │
    │ <span style="color: #ff00ff; text-decoration-color: #ff00ff; font-weight: bold">repr.tag_name                </span> │ bold bright_magenta                │
    │ <span style="color: #000000; text-decoration-color: #000000">repr.tag_contents            </span> │ default                            │
    │ <span style="font-weight: bold">repr.tag_end                 </span> │ bold                               │
    │ <span style="color: #808000; text-decoration-color: #808000">repr.attrib_name             </span> │ not italic yellow                  │
    │ <span style="font-weight: bold">repr.attrib_equal            </span> │ bold                               │
    │ <span style="color: #800080; text-decoration-color: #800080">repr.attrib_value            </span> │ not italic magenta                 │
    │ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">repr.number                  </span> │ bold not italic cyan               │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">repr.bool_true               </span> │ italic bright_green                │
    │ <span style="color: #ff0000; text-decoration-color: #ff0000; font-style: italic">repr.bool_false              </span> │ italic bright_red                  │
    │ <span style="color: #800080; text-decoration-color: #800080; font-style: italic">repr.none                    </span> │ italic magenta                     │
    │ <span style="color: #0000ff; text-decoration-color: #0000ff; text-decoration: underline">repr.url                     </span> │ not bold not italic underline      │
    │                               │ bright_blue                        │
    │ <span style="color: #ffff00; text-decoration-color: #ffff00">repr.uuid                    </span> │ not bold bright_yellow             │
    │ <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">repr.call                    </span> │ bold magenta                       │
    │ <span style="color: #800080; text-decoration-color: #800080">repr.path                    </span> │ magenta                            │
    │ <span style="color: #ff00ff; text-decoration-color: #ff00ff">repr.filename                </span> │ bright_magenta                     │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00">rule.line                    </span> │ bright_green                       │
    │ rule.text                     │ none                               │
    │ <span style="font-weight: bold">json.brace                   </span> │ bold                               │
    │ <span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">json.bool_true               </span> │ italic bright_green                │
    │ <span style="color: #ff0000; text-decoration-color: #ff0000; font-style: italic">json.bool_false              </span> │ italic bright_red                  │
    │ <span style="color: #800080; text-decoration-color: #800080; font-style: italic">json.null                    </span> │ italic magenta                     │
    │ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">json.number                  </span> │ bold not italic cyan               │
    │ <span style="color: #008000; text-decoration-color: #008000">json.str                     </span> │ not bold not italic green          │
    │ <span style="color: #000080; text-decoration-color: #000080; font-weight: bold">json.key                     </span> │ bold blue                          │
    │ prompt                        │ none                               │
    │ <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">prompt.choices               </span> │ bold magenta                       │
    │ <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">prompt.default               </span> │ bold cyan                          │
    │ <span style="color: #800000; text-decoration-color: #800000">prompt.invalid               </span> │ red                                │
    │ <span style="color: #800000; text-decoration-color: #800000">prompt.invalid.choice        </span> │ red                                │
    │ pretty                        │ none                               │
    │ <span style="color: #000080; text-decoration-color: #000080">scope.border                 </span> │ blue                               │
    │ <span style="color: #808000; text-decoration-color: #808000; font-style: italic">scope.key                    </span> │ italic yellow                      │
    │ <span style="color: #bfbf7f; text-decoration-color: #bfbf7f; font-style: italic">scope.key.special            </span> │ dim italic yellow                  │
    │ <span style="color: #800000; text-decoration-color: #800000">scope.equals                 </span> │ red                                │
    │ <span style="font-weight: bold">table.header                 </span> │ bold                               │
    │ <span style="font-weight: bold">table.footer                 </span> │ bold                               │
    │ table.cell                    │ none                               │
    │ <span style="font-style: italic">table.title                  </span> │ italic                             │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">table.caption                </span> │ dim italic                         │
    │ <span style="color: #800000; text-decoration-color: #800000; font-style: italic">traceback.error              </span> │ italic red                         │
    │ <span style="color: #ff0000; text-decoration-color: #ff0000">traceback.border.syntax_error</span> │ bright_red                         │
    │ <span style="color: #800000; text-decoration-color: #800000">traceback.border             </span> │ red                                │
    │ traceback.text                │ none                               │
    │ <span style="color: #800000; text-decoration-color: #800000; font-weight: bold">traceback.title              </span> │ bold red                           │
    │ <span style="color: #ff0000; text-decoration-color: #ff0000; font-weight: bold">traceback.exc_type           </span> │ bold bright_red                    │
    │ traceback.exc_value           │ none                               │
    │ <span style="color: #ff0000; text-decoration-color: #ff0000; font-weight: bold">traceback.offset             </span> │ bold bright_red                    │
    │ <span style="color: #3a3a3a; text-decoration-color: #3a3a3a">bar.back                     </span> │ grey23                             │
    │ <span style="color: #f92672; text-decoration-color: #f92672">bar.complete                 </span> │ rgb(249,38,114)                    │
    │ <span style="color: #729c1f; text-decoration-color: #729c1f">bar.finished                 </span> │ rgb(114,156,31)                    │
    │ <span style="color: #f92672; text-decoration-color: #f92672">bar.pulse                    </span> │ rgb(249,38,114)                    │
    │ progress.description          │ none                               │
    │ <span style="color: #008000; text-decoration-color: #008000">progress.filesize            </span> │ green                              │
    │ <span style="color: #008000; text-decoration-color: #008000">progress.filesize.total      </span> │ green                              │
    │ <span style="color: #008000; text-decoration-color: #008000">progress.download            </span> │ green                              │
    │ <span style="color: #808000; text-decoration-color: #808000">progress.elapsed             </span> │ yellow                             │
    │ <span style="color: #800080; text-decoration-color: #800080">progress.percentage          </span> │ magenta                            │
    │ <span style="color: #008080; text-decoration-color: #008080">progress.remaining           </span> │ cyan                               │
    │ <span style="color: #800000; text-decoration-color: #800000">progress.data.speed          </span> │ red                                │
    │ <span style="color: #008000; text-decoration-color: #008000">progress.spinner             </span> │ green                              │
    │ <span style="color: #008000; text-decoration-color: #008000">status.spinner               </span> │ green                              │
    │ tree                          │ none                               │
    │ tree.line                     │ none                               │
    │ markdown.paragraph            │ none                               │
    │ markdown.text                 │ none                               │
    │ <span style="font-style: italic">markdown.emph                </span> │ italic                             │
    │ <span style="font-weight: bold">markdown.strong              </span> │ bold                               │
    │ <span style="color: #ffffff; text-decoration-color: #ffffff; background-color: #000000">markdown.code                </span> │ bright_white on black              │
    │ <span style="color: #7fbfbf; text-decoration-color: #7fbfbf; background-color: #000000">markdown.code_block          </span> │ dim cyan on black                  │
    │ <span style="color: #800080; text-decoration-color: #800080">markdown.block_quote         </span> │ magenta                            │
    │ <span style="color: #008080; text-decoration-color: #008080">markdown.list                </span> │ cyan                               │
    │ markdown.item                 │ none                               │
    │ <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">markdown.item.bullet         </span> │ bold yellow                        │
    │ <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">markdown.item.number         </span> │ bold yellow                        │
    │ <span style="color: #808000; text-decoration-color: #808000">markdown.hr                  </span> │ yellow                             │
    │ markdown.h1.border            │ none                               │
    │ <span style="font-weight: bold">markdown.h1                  </span> │ bold                               │
    │ <span style="font-weight: bold; text-decoration: underline">markdown.h2                  </span> │ bold underline                     │
    │ <span style="font-weight: bold">markdown.h3                  </span> │ bold                               │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-weight: bold">markdown.h4                  </span> │ bold dim                           │
    │ <span style="text-decoration: underline">markdown.h5                  </span> │ underline                          │
    │ <span style="font-style: italic">markdown.h6                  </span> │ italic                             │
    │ <span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">markdown.h7                  </span> │ dim italic                         │
    │ <span style="color: #0000ff; text-decoration-color: #0000ff">markdown.link                </span> │ bright_blue                        │
    │ <span style="color: #000080; text-decoration-color: #000080">markdown.link_url            </span> │ blue                               │
    └───────────────────────────────┴────────────────────────────────────┘
    </pre>
