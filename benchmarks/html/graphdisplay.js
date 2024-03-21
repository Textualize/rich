'use strict';

$(document).ready(function() {
    /* The state of the parameters in the sidebar.  Dictionary mapping
       strings to arrays containing the "enabled" configurations. */
    var state = null;
    /* The name of the current benchmark being displayed. */
    var current_benchmark = null;
    /* An array of graphs being displayed. */
    var graphs = [];
    var orig_graphs = [];
    /* An array of commit revisions being displayed */
    var current_revisions = [];
    /* True when log scaling is enabled. */
    var log_scale = false;
    /* True when zooming in on the y-axis. */
    var zoom_y_axis = false;
    /* True when log scaling is enabled. */
    var reference_scale = false;
    /* True when selecting a reference point */
    var select_reference = false;
    /* The reference value */
    var reference = 1.0;
    /* Whether to show the legend */
    var show_legend = true;
    /* Is even commit spacing being used? */
    var even_spacing = false;
    var even_spacing_revisions = [];
    /* Is date scale being used ? */
    var date_scale = false;
    var date_to_revision = {};
    /* A little div to handle tooltip placement on the graph */
    var tooltip = null;
    /* X-axis coordinate axis in the data set; always 0 for
       non-parameterized tests where revision and date are the only potential x-axis */
    var x_coordinate_axis = 0;
    var x_coordinate_is_category = false;
    /* List of lists of value combinations to plot (apart from x-axis)
       in parameterized tests. */
    var benchmark_param_selection = [[null]];
    /* Highlighted revisions */
    var highlighted_revisions = null;
    /* Whether benchmark graph display was set up */
    var benchmark_graph_display_ready = false;


    /* UTILITY FUNCTIONS */
    function arr_remove_from(a, x) {
        var out = [];
        $.each(a, function(i, val) {
            if (x !== val) {
                out.push(val);
            }
        });
        return out;
    }

    function obj_copy(obj) {
        var newobj = {};
        $.each(obj, function(key, val) {
            newobj[key] = val;
        });
        return newobj;
    }

    function obj_length(obj) {
        var i = 0;
        for (var x in obj)
            ++i;
        return i;
    }

    function obj_get_first_key(data) {
        for (var prop in data)
            return prop;
    }

    function no_data(ajax, status, error) {
        $("#error-message").text(
            "No data for this combination of filters. ");
        $("#error").modal('show');
    }

    function get_x_from_revision(rev) {
        if (date_scale) {
            return $.asv.main_json.revision_to_date[rev];
        } else {
            return rev;
        }
    }

    function get_commit_hash(x) {
        // Return the commit hash in the current graph located at position x
        if (date_scale) {
            x = date_to_revision[x];
        }
        return $.asv.get_commit_hash(x);
    }


    function display_benchmark(bm_name, state_selection, highlight_revisions) {
        setup_benchmark_graph_display();

        $('#graph-display').show();
        $('#summarygrid-display').hide();
        $('#regressions-display').hide();
        $('.tooltip').remove();

        if (reference_scale) {
            reference_scale = false;
            $('#reference').removeClass('active');
            reference = 1.0;
        }
        current_benchmark = bm_name;
        highlighted_revisions = highlight_revisions;
        $("#title").text(bm_name);
        setup_benchmark_params(state_selection);
        replace_graphs();
    }

    function setup_benchmark_graph_display() {
        if (benchmark_graph_display_ready) {
            return;
        }
        benchmark_graph_display_ready = true;

        /* When the window resizes, redraw the graphs */
        $(window).on('resize', function() {
            update_graphs();
        });

        var nav = $("#graphdisplay-navigation");

        /* Make the static tooltips look correct */
        $('[data-toggle="tooltip"]').tooltip({container: 'body'});

        /* Add insertion point for benchmark parameters */
        var state_params_nav = $("<div id='graphdisplay-state-params'/>");
        nav.append(state_params_nav);

        /* Add insertion point for benchmark parameters */
        var bench_params_nav = $("<div id='graphdisplay-navigation-params'/>");
        nav.append(bench_params_nav);

        /* Benchmark panel */
        var panel_body = $.asv.ui.make_panel(nav, 'benchmark');

        var tree = $('<ul class="nav nav-list" style="padding-left: 0px"/>');
        var cursor = [];
        var stack = [tree];

        /* Sort keys for tree construction */
        var benchmark_keys = Object.keys($.asv.main_json.benchmarks);
        benchmark_keys.sort();

        /* Build tree */
        $.each(benchmark_keys, function(i, bm_name) {
            var bm = $.asv.main_json.benchmarks[bm_name];
            var parts = bm_name.split('.');
            var i = 0;
            var j;

            for (; i < cursor.length; ++i) {
                if (cursor[i] !== parts[i]) {
                    break;
                }
            }

            for (j = cursor.length - 1; j >= i; --j) {
                stack.pop();
                cursor.pop();
            }

            for (j = i; j < parts.length - 1; ++j) {
                var top = $(
                    '<li class="dropdown">' +
                        '<label class="nav-header"><b class="caret-right"/> ' + parts[j] +
                        '</label><ul class="nav nav-list tree" style="display: none;"/></li>');
                stack[stack.length - 1].append(top);
                stack.push($(top.children()[1]));
                cursor.push(parts[j]);

                $(top.children()[0]).on('click', function () {
                    $(this).parent().children('ul.tree').toggle(150);
                    var caret = $(this).children('b');
                    if (caret.attr('class') == 'caret') {
                        caret.removeClass().addClass("caret-right");
                    } else {
                        caret.removeClass().addClass("caret");
                    }
                });
            }

            var name = bm.pretty_name || parts[parts.length - 1];
            var top = $('<li><a href="#' + bm_name + '">' + name + '</li>');
            stack[stack.length - 1].append(top);

            top.tooltip({
                title: bm.code,
                html: true,
                placement: 'right',
                container: 'body',
                animation: 'false'
            });
        });

        panel_body.append(tree);

        $('#log-scale').on('click', function(evt) {
            log_scale = !evt.target.classList.contains("active");
            reference_scale = false;
            zoom_y_axis = false;
            $('#reference').removeClass('active');
            $('#zoom-y-axis').removeClass('active');
            reference = 1.0;
            update_state_url({'y-axis-scale': log_scale ? ['log']: []});
        });

        $('#zoom-y-axis').on('click', function(evt) {
            zoom_y_axis = !evt.target.classList.contains("active");
            reference_scale = false;
            log_scale = false;
            $('#reference').removeClass('active');
            $('#log-scale').removeClass('active');
            reference = 1.0;
            update_state_url({'y-axis-scale': zoom_y_axis ? ['zoom'] : []});
        });

        $('#reference').on('click', function(evt) {
            reference_scale = !evt.target.classList.contains("active");
            log_scale = false;
            zoom_y_axis = false;
            $('#log-scale').removeClass('active');
            $('#zoom-y-axis').removeClass('active');
            if (!reference_scale) {
                reference = 1.0;
                update_graphs();
            } else {
                $('#reference').popover({
                    content: 'Select a reference point',
                    placement: 'top',
                    container: 'body'});
                $('#reference').popover('show');
                reference = 1.0;
                select_reference = true;
            }
        });

        $('#even-spacing').on('click', function(evt) {
            even_spacing = !evt.target.classList.contains("active");
            date_scale = false;
            $('#date-scale').removeClass('active');
            update_state_url({'x-axis-scale': even_spacing ? ['even'] : []});
        });

        $('#date-scale').on('click', function(evt) {
            date_scale = !evt.target.classList.contains("active");
            even_spacing = false;
            $('#even-spacing').removeClass('active');
            update_state_url({'x-axis-scale': date_scale ? ['date'] : []});
        });

        $('#show-legend').on('click', function(evt) {
            show_legend = !show_legend;
            update_state_url({'show-legend': show_legend ? [] : [false]});
        });

        tooltip = $("<div></div>");
        tooltip.appendTo("body");

        /* The tooltip on a point shows the exact timing and the
           commit hash */
        function showTooltip(x, y, contents) {
            tooltip
                .css({
                    position: "absolute",
                    display: "none",
                    top: y - 4,
                    left: x - 2,
                    width: 4,
                    height: 4
                })
                .fadeIn(0)
                .tooltip({
                    title: contents,
                    html: true,
                    placement: 'top',
                    container: 'body',
                    animation: false
                })
                .tooltip('show');
        }

        var previous_hover = null;
        $("#main-graph").on("plothover", function (event, pos, item) {
            if (item) {
                if (previous_hover != item.datapoint) {
                    previous_hover = item.datapoint;
                    var y = item.datapoint[1];
                    var commit_hash = get_commit_hash(item.datapoint[0]);
                    if (commit_hash) {
                        var unit = $.asv.main_json.benchmarks[current_benchmark].unit;
                        showTooltip(
                            item.pageX, item.pageY,
                            $.asv.pretty_unit(y, unit) + " @ " + commit_hash);
                    }
                }
            } else {
                tooltip.tooltip("destroy");
            }
        });

        /* Clicking on a point should display the particular commit
           hash in another tab. */
        var previous_click;
        var previous_hash;
        $("#main-graph").on("plotclick", function (event, pos, item) {
            if (item) {
                if (previous_click != item.datapoint) {
                    previous_click = item.datapoint;
                    if (select_reference) {
                        $('#reference').popover('destroy');
                        select_reference = false;
                        reference = item.datapoint[1];
                        update_graphs();
                    } else {
                        var commit_hash = get_commit_hash(item.datapoint[0]);
                        if (previous_hash !== commit_hash) {
                            previous_hash = commit_hash;
                            window.open(
                                $.asv.main_json.show_commit_url + previous_hash,
                                '_blank');
                        }
                    }
                }
            }
        });
    }

    function setup_benchmark_params(state_selection) {
        if (!current_benchmark) {
            x_coordinate_axis = 0;
            x_coordinate_is_category = false;
            benchmark_param_selection = [[null]];
            return
        }

        /*
          Generic parameter selections
        */
        var index = $.asv.main_json;
        if (!state || state_selection !== null) {
            /*
               Setup the default configuration on first load,
               or when state selector is present
            */
            state = {};
            state.machine = index.params.machine;

            $.each(index.params, function(param, values) {
                state[param] = values;
                if (values.length > 1 && param !== 'machine') {
                    if (param == 'branch') {
                        state[param] = [values[0]];
                    }
                }
            });
        }

        if (state_selection !== null) {
            /* Select a specific generic parameter state */
            $.each(index.params, function(param, values) {
                if (state_selection[param]) {
                    state[param] = state_selection[param];
                }
            });
        }

        /*
          Benchmark-specific parameter selections
        */

        var params = index.benchmarks[current_benchmark].params;
        var param_names = index.benchmarks[current_benchmark].param_names;

        /* Default plot: time series */
        x_coordinate_axis = 0;
        if (state_selection['x-axis'] !== undefined &&
                state_selection['x-axis'] != "commit") {
            for (var k = 0; k < params.length; ++k) {
                if (state_selection['x-axis'] == param_names[k]) {
                    x_coordinate_axis = k + 1;
                    break;
                }
            }
        }

        /* Default plot: up to 8 lines */
        benchmark_param_selection = [[null]];
        if (params.length >= 1) {
            var count = 1;
            var max_curves = 8;

            for (var k = 0; k < params.length; ++k) {
                var param_name = param_names[k]
                var param_values = params[k]
                var item = [];
                if (state_selection['p-'+param_name] !== undefined) {
                    for (var j = 0; j < param_values.length; ++j) {
                        if (state_selection['p-'+param_name].includes(param_values[j])) {
                            item.push(j);
                        }
                    }
                } else {
                    for (var j = 0; j < param_values.length && (j+1)*count <= max_curves; ++j) {
                        item.push(j);
                    }
                }
                count = count * item.length;
                benchmark_param_selection.push(item);
            }
        }

        check_x_coordinate_axis();
        replace_params_ui();
        replace_benchmark_params_ui();
    }

    function update_state_url(params) {
        var info = $.asv.parse_hash_string(window.location.hash);
        $.each($.asv.main_json.params, function(param, values) {
            if (values.length > 1) {
                if (state[param].length != values.length || param == 'branch') {
                    info.params[param] = state[param];
                }
                else if (info.params[param]) {
                    delete info.params[param];
                }
            }
        });
        $.each(params || {}, function(key, value) {
            info.params[key] = value;
        });
        window.location.hash = $.asv.format_hash_string(info);
    }

    function replace_params_ui() {
        var index = $.asv.main_json;

        var nav = $('#graphdisplay-state-params');
        nav.empty();

        /* Machine selection */
        $.asv.ui.make_value_selector_panel(nav, 'machine', index.params.machine,  function(i, machine, button) {
            button.text(machine);

            if (index.params.machine.length > 1) {
                button.on('click', function(evt) {
                    if (!evt.target.classList.contains("active")) {
                        state.machine.push(machine);
                    } else {
                        state.machine = arr_remove_from(
                            state.machine, machine);
                    }
                    update_state_url();
                });
            }

            if ($.inArray(machine, state.machine) == -1) {
                button.removeClass('active');
            }

            /* Create tooltips for each machine */
            var details = [];
            $.each(index.machines[machine], function(key, val) {
                details.push(key + ': ' + val);
            });
            details = details.join('<br/>');

            button.tooltip({
                title: details,
                html: true,
                placement: 'right',
                container: 'body',
                animation: false
            });
        });

        /* Generic parameter selectors */
        $.each(index.params, function(param, values) {
            if (values.length > 1 && param != 'machine') {
                $.asv.ui.make_value_selector_panel(nav, param, values, function(i, value, button) {
                    var value_display;
                    if (value === null)
                        value_display = '[none]';
                    else if (!value)
                        value_display = '[default]';
                    else
                        value_display = value;

                    button.text(value_display);

                    if ($.inArray(value, state[param]) == -1) {
                        button.removeClass('active');
                    }

                    if (values.length > 1) {
                        button.on('click', function(evt) {
                            if (!evt.target.classList.contains("active")) {
                                state[param].push(value);
                            } else {
                                state[param] = arr_remove_from(
                                    state[param], value);
                            }
                            update_state_url();
                        });
                    }
                });
            }
        });
    }

    function replace_benchmark_params_ui() {
        var params = $.asv.main_json.benchmarks[current_benchmark].params;
        var param_names = $.asv.main_json.benchmarks[current_benchmark].param_names;

        /* Parameter selection UI */
        var nav = $('#graphdisplay-navigation-params');
        nav.empty();

        if (params.length == 0) {
            /* Simple time series: no need for parameter selection UI */
            $.asv.ui.reflow_value_selector_panels();
            return;
        }

        /* x-axis selector */
        {
            var axes = [];
            for (var axis = 0; axis < params.length + 1; ++axis) {
                axes.push(axis);
            }

            $.asv.ui.make_value_selector_panel(nav, "x-axis", axes, function (idx, axis, button) {
                var text;
                if (axis == 0) {
                    text = "commit";
                } else {
                    text = param_names[axis - 1];
                }
                if (x_coordinate_axis != axis) {
                    button.removeClass('active');
                }
                button.text(text);

                button.on('click', function (evt) {
                    $(evt.target).siblings().removeClass('active');
                    x_coordinate_axis = axis;
                    update_state_url({'x-axis': [text]});
                });
            });
        }

        /* Revision/commit value selector */
        if (x_coordinate_axis != 0) {
            /* Generate list of all revisions */
            var revisions = current_revisions.slice();
            revisions.sort();
            revisions.push(null);
            revisions.reverse();

            /* Add buttons */
            $.asv.ui.make_value_selector_panel(nav, "commit", revisions, function(idx, rev, button) {
                if (rev === null) {
                    button.text("last");
                } else {
                    var date_fmt = new Date($.asv.main_json.revision_to_date[rev]);
                    button.text($.asv.get_commit_hash(rev)
                                + " "
                                + date_fmt.toUTCString());
                }

                if ($.inArray(rev, benchmark_param_selection[0]) == -1) {
                    button.removeClass('active');
                }

                button.on('click', function(evt) {
                    var idx = $.inArray(rev, benchmark_param_selection[0]);
                    if (!evt.target.classList.contains("active")) {
                        if (idx == -1) {
                            benchmark_param_selection[0].push(rev);
                            benchmark_param_selection[0].sort();
                        }
                    } else {
                        if (idx != -1) {
                            benchmark_param_selection[0].splice(idx, 1);
                        }
                    }
                    replace_graphs();
                    update_graphs();
                });
            });
        }

        /* Parameters axes value selector */
        $.each(params, function(param_idx, values) {
            var axis = param_idx + 1;

            if (axis == x_coordinate_axis) {
                return;
            }

            name = param_names[param_idx];

            /* Add benchmark parameter selector */
            $.asv.ui.make_value_selector_panel(nav, name, values, function(value_idx, value, button) {
                var value_display;
                value_display = '' + $.asv.convert_benchmark_param_value(value);

                button.text(value_display);

                if ($.inArray(value_idx, benchmark_param_selection[axis]) == -1) {
                    button.removeClass('active');
                }

                button.on('click', function(evt) {
                    var new_selection = [];
                    var old_selection = benchmark_param_selection[param_idx+1];

                    if (!evt.target.classList.contains("active")) {
                        for (var k = 0; k < params[param_idx].length; ++k) {
                            if ($.inArray(k, old_selection) != -1 || k == value_idx) {
                                new_selection.push(k);
                            }
                        }
                    } else {
                        for (var k = 0; k < params[param_idx].length; ++k) {
                            if ($.inArray(k, old_selection) != -1 && k != value_idx) {
                                new_selection.push(k);
                            }
                        }
                    }
                    benchmark_param_selection[param_idx+1] = new_selection;
                    var new_selection_params = {};
                    new_selection_params['p-'+param_names[param_idx]] = new_selection.map(function(k) {
                        return params[param_idx][k];
                    });
                    update_state_url(new_selection_params);
                });
            });
        });

        $.asv.ui.reflow_value_selector_panels();
    }

    /* Check if x-axis is a category axis */
    function check_x_coordinate_axis() {
        if (!current_benchmark) {
            return;
        }

        var params = $.asv.main_json.benchmarks[current_benchmark].params;
        x_coordinate_is_category = false;
        if (x_coordinate_axis != 0) {
            for (var j = 0; j < params[x_coordinate_axis-1].length; ++j) {
                var value = $.asv.convert_benchmark_param_value(params[x_coordinate_axis-1][j]);
                if (typeof value != "number") {
                    x_coordinate_is_category = true;
                    break;
                }
            }
        }
    }

    function replace_graphs() {
        /* Given the settings in the sidebar, generate a list of the
           graphs we need to load. */
        function collect_graphs(current_benchmark, state, param_selection) {
            /* Given a specific group of parameters, generate the legend
               label to display for that line. Differences is an object of
               parameters that have different values across all graphs. */
            function graph_label(state, differences) {
                var ignore = {
                    'os': null,
                    'cpu': null,
                    'arch': null,
                    'ram': null
                };

                var parts = [];
                $.each(state, function(key, value) {
                    if (!ignore.hasOwnProperty(key) &&
                        differences.hasOwnProperty(key)) {
                        if (value === null) {
                            // missing key, skip
                        } else if (value) {
                            parts.push(key + "-" + value);
                        } else {
                            parts.push(key);
                        }
                    }
                });
                parts.sort();
                return parts.join('; ');
            }

            /* For a given parameter matrix, generate all permutations. */
            function permutations(matrix) {
                if (obj_length(matrix) === 0) {
                    return [{}];
                }

                matrix = obj_copy(matrix);
                var key = obj_get_first_key(matrix);
                var entry = matrix[key];
                delete matrix[key];

                var results = [];
                $.each(permutations(matrix), function(i, result) {
                    result = obj_copy(result);
                    if (entry.length) {
                        $.each(entry, function(i, value) {
                            result[key] = value;
                            results.push(obj_copy(result));
                        });
                    } else {
                        result[key] = null;
                        results.push(obj_copy(result));
                    }
                });

                results.sort();
                return results;
            }

            /* For all of the selected graphs, find out which parameters
               have different values across them.  We don't want to show
               parameters that are the same across all graphs in the
               legend labels, as that information is not really
               necessary. */
            function find_different_properties(graphs) {
                var different = {};
                var last_values = obj_copy(graphs[0]);
                $.each(graphs, function(i, graph) {
                    $.each(graph, function(key, val) {
                        if (last_values[key] != val) {
                            different[key] = true;
                        }
                    });
                });
                return different;
            }

            if (current_benchmark) {
                /* For the current set of enabled parameters, generate a
                   list of all the permutations we need to load. */
                var state_permutations = $.grep($.asv.main_json.graph_param_list, function (params) {
                    var ok = true;
                    $.each(state, function (key, values) {
                        if ($.inArray(params[key], values) == -1) {
                            ok = false;
                        }
                    });
                    return ok;
                });

                /* Find where the parameters are different. */
                var different = find_different_properties(state_permutations);
                /* For parameterized tests: names of benchmark parameters */
                var params = $.asv.main_json.benchmarks[current_benchmark].params;
                var param_names = $.asv.main_json.benchmarks[current_benchmark].param_names;
                /* Selected permutations of benchmark parameters, omitting x-axis */
                var selection = obj_copy(param_selection);
                selection[x_coordinate_axis] = [null]; /* value not referenced, set to null */
                var param_permutations = permutations(selection);

                /* Generate a main list of URLs and legend labels for
                   the graphs. */
                var all = [];
                $.each(state_permutations, function (i, perm) {
                    var graph_contents = [];
                    $.each(param_permutations, function(k, param_perm) {
                        /* For each state value, there can be several
                           benchmark parameter sets to plot */
                        var labels = obj_copy(perm);
                        for (var axis = 0; axis < params.length + 1; ++axis) {
                            if (axis != x_coordinate_axis) {
                                if (axis == 0) {
                                    /* Add time/commit value to the labels */
                                    var timestamp = param_perm[axis];
                                    different["commit"] = true;
                                    if (timestamp === null) {
                                        labels["commit"] = "last";
                                    }
                                    else {
                                        labels["commit"] = ""+$.asv.get_commit_hash(timestamp);
                                    }
                                }
                                else if (params[axis-1].length > 1) {
                                    /* Add parameter value to the labels */
                                    if (param_perm[axis] === null) {
                                        /* Empty permutation */
                                        return;
                                    }
                                    different[param_names[axis-1]] = true;
                                    labels[param_names[axis-1]] = "" + $.asv.convert_benchmark_param_value(params[axis-1][param_perm[axis]]);
                                }
                            }
                        }
                        graph_contents.push([param_perm,
                                             graph_label(labels, different)]);
                    });
                    all.push([$.asv.graph_to_path(current_benchmark, perm),
                              graph_contents]);
                });
                return all;
            } else {
                return [];
            }
        }

        /* Before loading graphs, remove any that are currently
           active. */
        graphs = [];
        orig_graphs = [];

        var to_load = collect_graphs(current_benchmark, state, benchmark_param_selection);
        var failures = 0;
        var count = 1;

        if (to_load.length === 0) {
            $('#main-graph').html("<div style='display: flex;" +
                "justify-content: center;" +
                " align-items: center; height: 100%;'>" +
                "<p style='font-size: 2rem;'>No graphs to load.</p>" +
                "</div>")
            return
        }

        current_revisions = [];
        $.each(to_load, function(i, item) {
            $.asv.load_graph_data(
                item[0]
            ).done(function (data) {
                $.each(data, function(i, point) {
                    if (current_revisions.indexOf(point[0]) === -1) {
                        current_revisions.push(point[0]);
                    }
                });
                $.each(item[1], function(j, graph_content) {
                    var series;
                    series = $.asv.filter_graph_data(data,
                                                     x_coordinate_axis,
                                                     graph_content[0],
                                                     $.asv.main_json.benchmarks[current_benchmark].params);
                    orig_graphs.push({
                        data: series,
                        label: graph_content[1],
                        bars: { order: count, },
                    });
                    count += 1;
                });
                graphs = orig_graphs;
                update_graphs();
            }).fail(function () {
                failures += 1;
                if (failures == to_load.length) {
                    /* If we don't get any results, we check that the
                    webserver is still live by loading a file we know
                    we have.  If that fails, too, then the webserver
                    is probably down. */
                    $.ajax({
                        url: "swallow.ico",
                        dataType: "text",
                        cache: false
                    }).done(function (index) {
                        update_graphs();
                        no_data();
                    }).fail(function () {
                        $.asv.ui.network_error();
                    });
                }
            });
        });
    }

    /* Handle log scaling the plot */
    function handle_y_scale(options) {
        if (!graphs.length)
            return;

        /* Find the minimum and maximum values */
        var min = Infinity;
        var max = -Infinity;
        var left = options.xaxis.min || 0;
        var right = options.xaxis.max || Infinity;

        $.each(graphs, function(i, graph) {
            var data = graph.data;
            var j = 0;
            if (!x_coordinate_is_category) {
                for (; j < data.length; ++j) {
                    var x = data[j][0];
                    if (x >= left) {
                        break;
                    }
                }
            }
            for (; j < data.length; ++j) {
                if (!x_coordinate_is_category) {
                    var x = data[j][0];
                    if (x >= right) {
                        break;
                    }
                }
                var p = data[j][1];
                if (p !== null && (!log_scale || p > 0)) {
                    if (p < min) {
                        min = p;
                    }
                    if (p > max) {
                        max = p;
                    }
                }
            }
        });

        if (!isFinite(min) || !isFinite(max)) {
            min = max = 1;
        }

        min /= reference;
        max /= reference;

        options.yaxis.min = min;
        options.yaxis.max = max;

        if (log_scale || reference_scale) {
            min = Math.floor(Math.log(min) / Math.LN10);
            max = Math.ceil(Math.log(max) / Math.LN10);

            if (min == max) {
                --min;
            }
            else if (reference_scale) {
                // Don't allow the reference level to be at graph top/bottom,
                // as this can look strange.
                if (min == 0) {
                    --min;
                }
                if (max == 0) {
                    ++max;
                }
            }

            var ticks = [];
            for (var x = min; x <= max; ++x) {
                ticks.push(Math.pow(10, x) * reference);
            }

            options.yaxis.ticks = ticks;
            options.yaxis.transform = function(v) {
                if (v <= 0) {
                    return null;
                } else {
                    return Math.log(v / reference) / Math.LN10;
                }
            };
            /* inverseTransform is required for plothover to work */
            options.yaxis.inverseTransform = function (v) {
                return Math.pow(10.0, v);
            };
            options.yaxis.tickDecimals = 3;
            options.yaxis.tickFormatter = function (v, axis) {
                return "10" + (
                    Math.round(
                        Math.log(v / reference) / Math.LN10)).toString().sup();
            };
            options.yaxis.min = Math.pow(10, min) * reference;
            options.yaxis.max = Math.pow(10, max) * reference;

            if (!reference_scale) {
                options.yaxis.axisLabel = $.asv.main_json.benchmarks[current_benchmark].unit;
            }
        }
        else {
            var unit = $.asv.main_json.benchmarks[current_benchmark].unit;
            var unit_list = null;

            if (unit == "seconds") {
                unit_list = $.asv.time_units;
            }
            else if (unit == "bytes") {
                unit_list = $.asv.mem_units;
            }

            if (unit_list !== null) {
                if (!zoom_y_axis) {
                    options.yaxis.min = 0.0;
                    options.yaxis.max = max * 1.3;
                }

                var unit_name = null;
                var multiplier = null;
                for (var i = 0; i < unit_list.length - 1; ++i) {
                    if (min < unit_list[i+1][2]) {
                        unit_name = unit_list[i][1];
                        multiplier = unit_list[i][2];
                        break;
                    }
                }
            }
            else {
                if (unit && unit != "unit") {
                    unit_name = unit;
                }
                multiplier = 1.0;
            }

            if (unit_name) {
                options.yaxis.axisLabel = unit_name;
                options.yaxis.tickFormatter = function (v, axis) {
                    return (v / multiplier).toPrecision(3);
                }
            }
        }
    }

    function even_spacing_transform(value) {
        /* Map timestamp value to commit index */
        for (var i = 0; i < even_spacing_revisions.length; i++) {
            if (value <= even_spacing_revisions[i]) {
                return i;
            }
        }
    }

    function even_spacing_inverseTransform(value) {
        /* Map commit index to timestamp value */
        for (var i = 0; i < even_spacing_revisions.length; i++) {
            if (value <= i) {
                return even_spacing_revisions[i];
            }
        }
    }

    function handle_x_scale(options) {
        if (!graphs.length)
            return;

        if (x_coordinate_axis == 0) {
            if (!date_scale) {
                // restore original graphs
                graphs = orig_graphs;
                options.xaxis.mode = null;
                options.xaxis.axisLabel = 'commits';
                options.xaxis.tickFormatter = function (v, axis) { return ""; };
            }
            if (even_spacing) {
                even_spacing_revisions = [];
                $.each(graphs, function(i, graph) {
                    var data = graph.data;
                    for (var j = 0; j < data.length; ++j) {
                        if (even_spacing_revisions.indexOf(data[j][0]) === -1) {
                            even_spacing_revisions.push(data[j][0]);
                        }
                    }
                });
                even_spacing_revisions.sort(function(a, b) { return a - b; });
                options.xaxis.transform = even_spacing_transform;
                /* inverseTransform is required for plothover to work */
                options.xaxis.inverseTransform = even_spacing_inverseTransform;
            } else if (date_scale) {
                options.xaxis.mode = 'time';
                options.xaxis.axisLabel = 'commit date';
                options.xaxis.tickFormatter = null;

                // deep copy graphs and transform into time series data
                graphs = $.extend(true, [], orig_graphs);
                date_to_revision = {};
                $.each(graphs, function(i, graph) {
                    $.each(graph.data, function(j, point) {
                        var date = $.asv.main_json.revision_to_date[point[0]];
                        date_to_revision[date] = point[0];
                        point[0] = date;
                    });
                    graph.data.sort(function(a, b) { return a[0] - b[0]; });
                });
            }
        } else {
            if (x_coordinate_is_category) {
                options.xaxis.mode = 'categories';
                options.xaxis.tickLength = 0;
                options.series = {
                    bars: {
                        show: true,
                        barWidth: 0.6 / graphs.length,
                        align: "center"
                    }
                };

                // deep copy graphs and html-escape x-labels
                graphs = $.extend(true, [], orig_graphs);
                $.each(graphs, function(i, graph) {
                    $.each(graph.data, function(j, point) {
                        point[0] = $("<span>").text('' + point[0]).html();
                    });
                });
            }
            else {
                graphs = orig_graphs;
            }
            var param_names = $.asv.main_json.benchmarks[current_benchmark].param_names;
            options.xaxis.axisLabel = param_names[x_coordinate_axis-1];
        }
    }

    /* Once we have all of the graphs loaded, send them to flot for
       drawing. */
    function update_graphs() {
        if (current_benchmark === null) {
            return;
        }

        var markings = [];

        if (x_coordinate_axis == 0) {
            $.each($.asv.main_json.tags, function(tag, revision) {
                var x = get_x_from_revision(revision);
                markings.push(
                    { color: "#ddd", lineWidth: 1, xaxis: { from: x, to: x } }
                );
            });

            if (highlighted_revisions) {
                $.each(highlighted_revisions, function(i, revs) {
                    var x_values = [];
                    $.each(revs, function(i, rev) {
                        var x = get_x_from_revision(rev);
                        markings.push(
                            { color: '#d00', lineWidth: 2, xaxis: { from: x, to: x } }
                        );
                        x_values.push(x);
                    });
                    if (revs.length > 1) {
                        markings.push(
                            { color: "rgba(200, 0, 0, 0.2)", alpha: 0.5, lineWidth: 2,
                              xaxis: { from: Math.min.apply(null, x_values),
                                       to: Math.max.apply(null, x_values) }}
                        );
                    }
                });
            }
        }

        var unit;
        if (reference_scale) {
            unit = 'relative';
        } else {
            unit = $.asv.main_json.benchmarks[current_benchmark].unit;
        }

        var options = {
            colors: $.asv.colors,
            series: {
                lines: {
                    show: true,
                    lineWidth: 1
                },
                points: {
                    show: true
                },
                shadowSize: 0
            },
            grid: {
                hoverable: true,
                clickable: true,
                markings: markings
            },
            xaxis: {
                tickLength: 5,
                axisLabel: "",
                axisLabelUseCanvas: true,
                axisLabelFontFamily: "sans-serif",
                axisLabelFontSizePixels: 12
            },
            yaxis: {
                axisLabel: "",
                axisLabelUseCanvas: true,
                axisLabelFontFamily: "sans-serif",
                axisLabelFontSizePixels: 12
            },
            selection: {
                mode: "x"
            },
            legend: {
                show: show_legend,
                position: "nw",
                labelFormatter: function(label, series) {
                    // Ensure HTML escaping
                    return $("<span>").text(label).html();
                }
            }
        };

        handle_x_scale(options);
        handle_y_scale(options);

        var graph_div = $('#main-graph');
        var overview_div = $('#overview');

        var plot = $.plot(graph_div, graphs, options);

        /* Set up the "overview" plot */
        var overview = null;

        if (x_coordinate_axis != 0) {
            /* Overview is useful mostly for the time axis */
            overview_div.empty();
        }  else {
            var overview_options = {
                colors: $.asv.colors,
                series: {
                    lines: {
                        show: true,
                        lineWidth: 1
                    },
                    shadowSize: 0
                },
                xaxis: {
                    ticks: [],
                    mode: "time"
                },
                yaxis: {
                    ticks: [],
                    min: 0,
                    autoscaleMargin: 0.1
                },
                selection: {
                    mode: "x"
                },
                legend: {
                    show: false
                }
            };
            if (even_spacing) {
                overview_options.xaxis.transform = even_spacing_transform;
                overview_options.xaxis.inverseTransform = even_spacing_inverseTransform;
            }
            overview = $.plot(overview_div, graphs, overview_options);
        }

        graph_div.off("plotselected");
        graph_div.on("plotselected", function (event, ranges) {
            // do the zooming
            var new_options = $.extend(true, {}, options, {
                xaxis: {
                    min: ranges.xaxis.from,
                    max: ranges.xaxis.to
                }
            });

            handle_y_scale(new_options);

            plot = $.plot(graph_div, graphs, new_options);

            // Update things that depend on the range
            update_tags();
            update_range();

            // don't fire event on the overview to prevent eternal loop
            if (overview) {
                overview.setSelection(ranges, true);
            }
        });

        overview_div.off("plotselected");
        overview_div.on("plotselected", function (event, ranges) {
            plot.setSelection(ranges);
            // Update things that depend on the range
            update_tags();
            update_range();
        });

        function update_range() {
            if (x_coordinate_axis != 0) {
                /* Only applies when x-axis is the time axis */
                return;
            }

            /* Find the minimum and maximum values */
            var min = Infinity;
            var left = plot.getAxes().xaxis.min;
            $.each(graphs, function(i, graph) {
                var data = graph.data;
                for (var j = 0; j < data.length; ++j) {
                    var p = data[j][0];
                    if (p !== null && p >= left) {
                        if (p < min) {
                            min = p;
                        }
                        break;
                    }
                }
            });

            var max = -Infinity;
            var right = plot.getAxes().xaxis.max;
            $.each(graphs, function(i, graph) {
                var data = graph.data;
                for (var j = data.length - 1; j >= 0; --j) {
                    var p = data[j][0];
                    if (p !== null && p <= right) {
                        if (p > max) {
                            max = p;
                        }
                        break;
                    }
                }
            });

            var result;
            if (min === null || max === null || min > max) {
                result = '';
            } else if (min == max) {
                result = get_commit_hash(min) + '^!';
            } else {
                var first_commit = get_commit_hash(min);
                var last_commit = get_commit_hash(max);
                result = first_commit + ".." + last_commit;
            }
            $("#range")[0].value = result;
        }

        function update_tags() {
            if (x_coordinate_axis != 0) {
                /* Only applies when x-axis is the time axis */
                return;
            }

            /* Add the tags as vertical grid lines */
            var canvas = plot.getCanvas();
            var xmin = plot.getAxes().xaxis.min;
            var xmax = plot.getAxes().xaxis.max;
            $.each($.asv.main_json.tags, function(tag, revision) {
                var x = get_x_from_revision(revision);
                if (x >= xmin && x <= xmax) {
                    var p = plot.pointOffset({x: x, y: 0});

                    graph_div.append(
                        "<div style='position:absolute;" +
                            "left:" + p.left + "px;" +
                            "top: -2ex;" +
                            "color:#666;background:white;padding-left:0.25em;font-size:smaller;'>" + tag + "</div>");
                }
            });
        }

        update_tags();
        update_range();
    }


    $.asv.register_page('graphdisplay', function(params) {
        var benchmark = params['benchmark'];
        var highlight_revisions = null;
        var state_selection = null;

        if (params['commits']) {
            highlight_revisions = [];
            $.each(params['commits'], function(i, value) {
                var match = value.match(/^([a-z0-9]+)-([a-z0-9]+)$/);
                if (match) {
                    highlight_revisions.push([$.asv.get_revision(match[1]), $.asv.get_revision(match[2])]);
                }
                else {
                    highlight_revisions.push([$.asv.get_revision(value)]);
                }
            });
            delete params['commits'];
        }

        if (params['y-axis-scale']) {
            if (params['y-axis-scale'][0] === 'log') {
                $('#log-scale').addClass('active');
                log_scale = true;
            } else if (params['y-axis-scale'][0] === 'zoom') {
                $('#zoom-y-axis').addClass('active');
                zoom_y_axis = true;
            }
            delete params['y-axis-scale'];
        }

        if (params['x-axis-scale']) {
            if (params['x-axis-scale'][0] === 'even') {
                $('#even-spacing').addClass('active');
                even_spacing = true;
            } else if (params['x-axis-scale'][0] === 'date') {
                $('#date-scale').addClass('active');
                date_scale = true;
            }
            delete params['x-axis-scale'];
        }

        var show_legend_button = $('#show-legend')
        if (params['show-legend']) {
            if (params['show-legend'][0] === 'false') {
                show_legend = false;
                show_legend_button.removeClass('active');
            }
            else {
                show_legend_button.addClass('active');
                show_legend = true;
            }
            delete params['show-legend'];
        }
        else {
            show_legend_button.addClass('active');
        }

        if (Object.keys(params).length > 0) {
            state_selection = params;
        }

        display_benchmark(benchmark, state_selection, highlight_revisions);
    });
});
